from flask import Flask, jsonify, redirect
from app.models import db
from app.resources import Auth, Register, Words, api, jwt


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config["JWT_SECRET_KEY"] = "o-secret-key"  # Change this!

    api.add_resource(Auth, "/login")
    api.add_resource(Register, "/register")
    api.add_resource(Words, "/words")

    db.init_app(app)
    api.init_app(app)
    jwt.init_app(app)

    @app.route("/")
    def home():
        return redirect('https://github.com/DavidTbilisi/mnmwords')

    @app.before_first_request
    def before_first_request():
        db.create_all()

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)