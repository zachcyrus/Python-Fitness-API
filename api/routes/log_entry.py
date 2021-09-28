from logging import log
from flask import (Blueprint, request)
from flask_restx import  Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utils.auth_functions import verify_user

from api.models.models import User

log_entry = Namespace('logs', description="Endpoint for user routine exercises logs")


@log_entry.route('/')
class LogInput(Resource):
    @jwt_required()
    @verify_user
    def get(self):
        '''Testing util functions'''
        user_id = get_jwt_identity()

        current_user = User.find_user_by_id(user_id)
        
        name_of_user = current_user.name
        return {
            'success': 'Verify function is working',
            "name": name_of_user
        },200

    @jwt_required()
    def post(self):
        '''Route to add completed exercises to route'''
        return {
            'testing': "Testing route"

        },200