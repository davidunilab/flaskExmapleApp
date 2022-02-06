from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash
from app.models import UserModel, db


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

