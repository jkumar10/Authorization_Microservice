from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

app=Flask(__name__)
CORS(app)

api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///carpoolusers.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'my-secret-string'

db = SQLAlchemy(app)

@app.before_first_request
def create_tables():
    db.create_all()

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

import views, models, resources

api.add_resource(resources.UserRegistration, '/registration')
api.add_resource(resources.UserLogin, '/login')
