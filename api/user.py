# File for defining user API endpoint functions
from flask import (Blueprint, request)

bp = Blueprint('user', __name__, url_prefix='/user')

# Temp list of users while db isn't up yet

user_list = [
    {
        "user_name": "First-User",
        "name": "Blake",
        "stats": "Top 0.1%",
    },
    {
        "user_name": "Fake",
        "name": "Andrew",
        "stats": "Top 10%"
    }
]

# function to add a user to user_list
def add_user(req):

    new_user = {
        "user_name":req["user_name"],
        "name":req["name"],
        "stats":req["stats"]
    }

    user_list.append(new_user)


#blueprint routes

@bp.route('/')
def user_info():
    if request.method == 'GET':
        return "Welcome to the user api route"

#route to register a new user/add to set
@bp.route('/register')
def register_user():
    if request.method == 'POST':
        # Check if request body contains JSON
        if request.is_json:

            user_data = request.get_json()

            add_user(user_data)

            return "User Signed Up", 200

        # If doesn't contain JSON return error
        else:
            return "Post request must contain JSON",  400

