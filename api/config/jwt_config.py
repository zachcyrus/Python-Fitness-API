from api.models.models import User
from bcrypt import checkpw

def authenticate(username, password):
    user = User.find_username(username)
    if user and checkpw(password.encode('utf8'), user.password):
        return user

def identity(payload):
    user_id = payload['identity']
    return User.find_user_by_id(user_id)