# File for defining user API endpoint functions
from flask import (Blueprint, request)
from flask_restx import  Resource, Namespace, fields


from api.models.models import User

user = Namespace('user', path='/user')


# Route to delete user from db/set
@user.route('/delete/<int:user_id>')
class DeleteUser(Resource):
    def delete(self,user_id):
        if request.method != "DELETE":
            return {"Only delete method allowed for this route"}, 400
        else:
            user_to_delete = User.find_user_by_id(user_id)
            if user_to_delete:
                user_to_delete.delete_user()
                return {
                    "success":"Deleted User"
                }, 200

            else:
                return {
                    "error": "User with that id not found"
                }, 400
