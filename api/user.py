# File for defining user API endpoint functions
from flask import (Blueprint, request)

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/')
def user_info():
    if request.method == 'GET':
        return "Welcome to the user api route"