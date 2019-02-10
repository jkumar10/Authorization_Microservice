from flask_restful import Resource, reqparse
from models import UserModel
from flask_jwt_extended import (create_access_token, get_jwt_identity, get_raw_jwt)


# This class is used to register the user in the database. It takes in the parameters from the
# api calls and then saves the information by calling correspoding db method and returns a token.
class UserRegistration(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', help = 'Email cannot be blank', required = True)
        parser.add_argument('name', help = 'Name cannot be blank', required = True)
        parser.add_argument('password', help = 'Password cannot be blank', required = True)
        data = parser.parse_args()
        if UserModel.search_email(data['email']):
          return {'message': 'User {} already exists'. format(data['email'])}

        new_user = UserModel(
            email = data['email'],
            name = data['name'],
            password = UserModel.encrypt_password(data['password'])
        )
        try:
            new_user.save_info()
            access_token = create_access_token(identity = data['email'])
            return {
                'message': 'User {} was created'.format( data['email']),
                'access_token': access_token
            }
        except:
            return {'message': 'Error encountered'}, 500


# This class is used to verify the input calls from the user and if verified logs the user into the applicationself.
# It calls external methods to verify the credentials of the user and creates the access token for the user.
class UserLogin(Resource):
    def post(self):
        loginparser = reqparse.RequestParser()
        loginparser.add_argument('email', help = 'Email cannot be blank', required = True)
        loginparser.add_argument('password', help = 'Password cannot be blank', required = True)
        data = loginparser.parse_args()
        current_user = UserModel.search_email(data['email'])
        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['email'])}


        if UserModel.check_password(data['password'], current_user.password):
            access_token = create_access_token(identity = data['email'])
            return {
                    'message': 'Logged in as {}'.format(current_user.email),
                    'access_token': access_token,
                    'id':current_user.id,
                    'email': current_user.email,
                    'name':current_user.name
                   }
        else:
            return {'message': 'Wrong password'}



# Based on the reference flask architecture given on https://codeburst.io/jwt-authorization-in-flask-c63c1acf4eeb
