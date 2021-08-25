# File for defining user API endpoint functions
from flask import (Blueprint, request, jsonify)

from api.models.models import User

bp = Blueprint('user', __name__, url_prefix='/user')

# function to add a user to user_list and save to db.


def add_user(req):

    new_user = {
        "user_name": req["user_name"],
        "name": req["name"],
        "stats": req["stats"],
        "email": req["email"]
    }

    saved_user = User(new_user)

    saved_user.save_to_db()


# blueprint routes

@bp.route('/')
def user_info():
    if request.method == 'GET':
        all_users = User.select_all()
        return {
            "all_users": all_users
        }, 200

# route to register a new user/add to set


@bp.route('/register', methods=["POST"])
def register_user():
    global global_id

    if request.method == 'POST':

        # Check if request body contains JSON

        if request.is_json:

            user_data = request.get_json()

            # Check if request contains the right parameters

            if user_data.keys() == {"user_name", "stats", "name"}:

                # Check if someone with that user_name already exists

                if User.find_username(user_data["user_name"]):
                    return {
                        "error": "User with that username already exists"
                    }, 400
                else:

                    add_user(user_data)

                    return {
                        "success": "User Signed Up",
                        "new_user": user_data
                    }, 200

            else:
                return {
                    "error": "Request is missing the required parameters"
                }, 400

        # If request doesn't contain JSON return error
        else:
            return {"Post request must contain JSON"},  400

    # Request method isn't post
    else:
        return {
            "error": "Request method must be post",
        }, 400


# Route to delete user from db/set
@bp.route('/delete/<int:user_id>', methods=["DELETE"])
def delete_user(user_id):
    if request.method != "DELETE":
        return {"Only delete method allowed for this route"}, 400
    else:
        for i,  user in enumerate(user_list):
            if user["id"] == user_id:
                del user_list[i]

                return {
                    "success": "user was deleted"
                }, 200
        return {
            "error": "User with that id not found"
        }, 400
