from werkzeug.security import check_password_hash
from flask import Blueprint, request
from flask_restx import  Resource, Namespace, fields

from api.models.models import User

# Route for authentication

auth = Namespace('Auth', 'Authentication route for users')

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

@auth.route('/signup')
class Signup(Resource):

    @auth.expect(user_model)
    def post(self):
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
                    "new_user": new_user,
                    "user_id": saved_user.user_id
                }, 200
                
            except Exception as e:
                return {
                    "error": "Error saving user to database",
                    "details":e
                }, 400