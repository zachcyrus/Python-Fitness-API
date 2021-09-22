from flask import Blueprint, request
from flask_restx import  Resource, Namespace, fields
from flask_jwt_extended import create_access_token
from flask_restx.marshalling import marshal_with
from api.models.models import User

# Route for authentication

auth = Namespace('Auth', 'Authentication route for to signup and login')

user_model = auth.model(
    "New User Model",
    {
        "user_name": fields.String(
            required=True,
            description='Username selected',
            help="Username cannot be blank"
        ),
        "password": fields.String(
            required=True,
            description='Password for account',
            help="Every user needs a password"
        ),
        "email": fields.String(
            required=True,
            description="Email associated with the account",
            help="Email is required"
        ),
        "name": fields.String(
            required=True,
            description='Full name or first name of the user',
            help='Name associated with the account'
        )
    }
)

returned_user_model = auth.model(
    "Successful User Signup",
    {
        "success": fields.String(default="New User signed up"),
        "password": fields.String,
        "user_id": fields.Integer
    }
)

login_success_model = auth.model(
    "Successful User Login",
    {
        "access_token": fields.String
    }
)

login_payload = auth.model(
    "User model for logging in",
    {
        "user_name": fields.String(
            required=True,
            description='Username selected',
            help="Username cannot be blank"
        ),
        "password": fields.String(
            required=True,
            description='Password for account',
            help="Every user needs a password"
        ),
    }
)

@auth.route('/signup')
class Signup(Resource):
    
    @auth.expect(user_model)
    @auth.response(200, "Success", returned_user_model)
    def post(self):
        '''
        Route for user signup 
        '''
        # expect a POST request with a response body containing username, password, and email
        if request.method != 'POST' or not(request.is_json):
            return {
                "error": "Must be a POST request and contain JSON"
            },400
        elif ('user_name' or 'password' or 'email' or 'name') not in request.json:
            return {
                "error": "Request body must contain username, password, and email"
            }, 400

        else:
            

            try:
                new_user = request.json

                saved_user = User(new_user)

                saved_user.save_to_db()

                return {
                    "success": "New User signed up",
                    "password": saved_user.password,
                    "user_id": saved_user.user_id
                }, 200
                
            except Exception as e:
                return {
                    "error": "Error saving user to database",
                    "details":str(e)
                }, 400

# create a login route that returns jwt
@auth.route('/login')
class Login(Resource): 
    @auth.expect(login_payload)
    @auth.response(200, "Success", login_success_model)
    def post(self):
        '''
        Login route that returns jwt on authentication
        '''
        if('user_name' or 'password') not in request.json:
            return {
                "error":"Request must contain either user_name and password"
            },400

        user_request = request.json

        user_in_db = User.find_username(user_request['user_name'])

        if user_in_db is False:
            return {
                "error": "User not found in database"
            },400

        elif user_in_db.check_password(user_request['password']) is False:
            return {
                "error": "Password does not match what's in database"
            },400
        else:
            jwt_token = create_access_token(identity=user_in_db.user_id)
            return {
                "access_token": jwt_token
            }, 200

    
