from os import path
from flask import Blueprint
from flask_restx import Api


api_bp = Blueprint('api', __name__)
api = Api(api_bp,title='Python Fitness API', description="Python API meant to show users different endpoints")


# Adding routes

from api.routes.auth import auth
api.add_namespace(auth,path='/auth')

from api.routes.exercises import exercise
api.add_namespace(exercise,path='/exercise')

from api.routes.routines import routines
api.add_namespace(routines,path='/routines')