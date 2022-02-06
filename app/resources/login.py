from flask import jsonify
from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from werkzeug.security import check_password_hash

from app.models import UserModel, db

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
        # print(access_token)
        return jsonify(access_token=access_token)

