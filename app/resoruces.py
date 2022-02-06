from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask import Flask, jsonify, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from app.models import UserModel, WordModel, db

jwt = JWTManager()
api = Api()

word_fields = {
    "word": fields.String,
    "translation": fields.String,
    "assoc": fields.String,
    "connection": fields.String,
    "examples": fields.String,
    "link": fields.String,
    "id": fields.Integer,
}

wordParser = reqparse.RequestParser()
wordParser.add_argument("word")
wordParser.add_argument("translation")
wordParser.add_argument("assoc")
wordParser.add_argument("connection")
wordParser.add_argument("examples")
wordParser.add_argument("link")
wordParser.add_argument("id")


class Auth(Resource):
    def post(self):
        loginParser = reqparse.RequestParser()
        loginParser.add_argument("email")
        loginParser.add_argument("password")
        args = loginParser.parse_args()


        user = UserModel.query.filter_by(email=args["email"]).first()


        if user == None:
            return {"msg": "Email was not found"}

        if args["email"] != user.email or not check_password_hash(user.password, args["password"]):
            return jsonify({"msg": "Bad username or password"}), 401

        access_token = create_access_token(identity=user.id)
        print(access_token)

        return jsonify(access_token=access_token)


class Register(Resource):
    def post(self):
        registerParser = reqparse.RequestParser()
        registerParser.add_argument("username")
        registerParser.add_argument("email")
        registerParser.add_argument("password")
        args = registerParser.parse_args()

        user = UserModel(
            username=args['username'],
            email=args['email'],
            password=generate_password_hash(args['password'])
        )

        db.session.add(user)
        db.session.commit()
        return {"msg": "created"}, 201



class Words(Resource):
    @jwt_required()
    def post(self):
        args = wordParser.parse_args()

        word = WordModel(
            word=args['word'],
            translation=args['translation'],
            assoc=args['assoc'],
            connection=args['connection'],
            user_id=get_jwt_identity()
        )
        db.session.add(word)
        db.session.commit()
        return jsonify({"msg": "new word has been added to db"})

    @marshal_with(word_fields)
    @jwt_required()
    def get(self):
        args = wordParser.parse_args()
        word = WordModel.query.filter_by(user_id=get_jwt_identity())

        if args["word"] != None:
            return word.filter_by(word=args['word']).first()
        elif args["id"] != None:
            return word.filter_by(id=args['id']).first()
        elif args["assoc"] != None:
            return word.filter_by(assoc=args['assoc']).first()
        elif args["translation"] != None:
            return word.filter_by(translation=args['translation']).first()
        else:
            return word.all()

    @jwt_required()
    def put(self):
        args = wordParser.parse_args()
        word = WordModel.query.filter_by(user_id=get_jwt_identity()).filter_by(id=args['id']).first()
        for arg in word_fields.keys():
            if args[arg] != None:
                setattr(word, arg, args[arg])
        db.session.add(word)
        db.session.commit()
        return jsonify({"msg": "word has been updated"})


    @jwt_required()
    def delete(self):
        args = wordParser.parse_args()
        word = WordModel.query.filter_by(user_id=get_jwt_identity()).filter_by(word=args['word']).first()
        db.session.delete(word)
        db.session.commit()
        return jsonify({"msg": "word has been deleted"})

