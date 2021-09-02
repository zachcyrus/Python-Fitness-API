from werkzeug.security import check_password_hash
from flask import Blueprint, request

from api.models.models import User

# Route for authentication

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/signup', methods=["POST"])
def user_sign_up():

    # expect a POST request with a response body containing username, password, and email
    if request.method != 'POST' or not(request.is_json):
        return {
            "error": "Must be a POST request and contain JSON"
        },400
    elif ('username' or 'password' or 'email') not in request.json:
        return {
            "error": "Request body must contain username, password, and email"
        }, 400

    else:
        

        try:
            new_user = request.is_json

            saved_user = User(new_user)

            saved_user.save_to_db()

            return {
                "success": "New User signed up",
                "new_user": new_user
            }, 200
            
        except :
            return {
                "error": "Error saving user to database"
            }, 400

        






    