from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask import Flask, jsonify, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, JWTManager
from app.models import UserModel, WordModel, db
from app.resources.words import Words
from app.resources.login import Auth
from app.resources.register import Register

jwt = JWTManager()
api = Api()