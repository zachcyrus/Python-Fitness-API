from api.models.models import Routines, User_Routines, User
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

# Decorator meant to ensure that a user with an ID retrieved from a jwt actually exists
def verify_user(f):
    @wraps(f)
    def verify_user_function(*args, **kwargs):

        user_id = get_jwt_identity()
        current_user = User.find_user_by_id(user_id)

        if current_user is False:
            return {
                "error": "User with that ID not found"
            }, 400
        else:
            return f(*args, **kwargs)

    return verify_user_function

