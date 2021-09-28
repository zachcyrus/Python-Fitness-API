from logging import log
from os import path
from flask import Blueprint
from flask_restx import Api

authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization',
        'description': "Type in the *'Value'* input box below: **'Bearer &lt;JWT&gt;'**, where JWT is the token"
    }
}

api_bp = Blueprint('api', __name__)
api = Api(api_bp,title='Python Fitness API', description="Python API meant to show users different endpoints", authorizations=authorizations)


# Adding routes

from api.routes.auth import auth
api.add_namespace(auth,path='/auth')

from api.routes.exercises import exercise
api.add_namespace(exercise,path='/exercise')

from api.routes.routines import routines
api.add_namespace(routines,path='/routines')

from api.routes.log_entry import log_entry
api.add_namespace(log_entry,path='/logs')