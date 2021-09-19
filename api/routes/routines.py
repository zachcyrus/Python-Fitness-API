# Route for defining routines endpoints

from operator import add
from flask import (request)
from flask_restx import  Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.models.models import Routines, User_Routines, User

routines = Namespace('Routines', "Route for managing routines for different users")

def add_routine(req):
    routine_dict = {
        "routine_name": req["routine_name"],
        "routine_description": req["routine_description"]
    }

    try:
        saved_routine = Routines(routine_dict)
        saved_routine.save_routine()
        return saved_routine.routine_id
    except Exception as e:
        return ('Error saving',str(e))

@routines.route('/')
class RoutineTest(Resource):
    def get(self):
        # possibly return all user submitted routines
        try:
            return {
                "all_routines": Routines.get_all_routines()
            }, 200
        except:
            return {
                "error": "Error occurred retrieving data from DB"
            }, 400

#get routines for specific user 
#Protected route
@routines.route('/self')
class UserRoutines(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()

        current_user = User.find_user_by_id(user_id)

        if current_user is False:
            return {
                "error": "User with that ID not found"
            }, 400

        else:
            return {
                "user":user_id,
                "user_routine":current_user.get_routines()
            },200
        

#get specific routine with exercises for a particular user 
@routines.route('/<int:user_id>/<string:routine_name>')
class UserRoutineExercises(Resource): 
    def get(self,user_id, routine_name):
        current_user = User.find_user_by_id(user_id)

        if current_user is False:
            return {
                "error": "User with that ID not found"
            }, 400

        elif current_user.find_routine(routine_name) is False:

            return {
                    "error": "Routine not found associated with that user_id"
                }, 400

        else:
            current_user_routine = current_user.find_routine(routine_name)


            exercises_in_routine = current_user_routine.get_exercises_in_routine()

            return {
                "routine_name":current_user_routine.routine_name,
                "routine_description": current_user_routine.routine_description,
                "exercises_list": exercises_in_routine
            }, 200


#Route for addding a routine to a particular user
@routines.route('/add/<int:user_id>', methods=["POST"])
class AddUserRoutine(Resource):

    def post(self,user_id):
        if request.method != 'POST' or not(request.is_json):
            return {
                "error": "Request must be a POST method, and request must contain JSON"
            }, 400

        elif ('routine_description' or "routine_name") not in request.json:
            return {
                "error": "Request must contain a routine_description and routine_name"
            }, 400

        
        # Check if user exists

        elif User.find_user_by_id(user_id) == False:
            return {
                "error": "User with that id not found "
            }, 400

        else:
            user_routine = request.json


            try:
                # Saving the routine id from the newly created routine
                created_routine_id = add_routine(user_routine)
                print(created_routine_id)

                # Add the routine to the user_routine Table 
                # 1. Add the routine to the user instance with that id 

                new_selected_user_routine = User_Routines(user_id=user_id,routine_id=created_routine_id)

                new_selected_user_routine.save_user_routine()

                return {
                    "success":f"Routine added to {user_id}",
                    "routine": user_routine
                }, 200

            except Exception as e:
                return {
                    "error": "Error creating routine table please try again",
                    "details":str(e)
                },400


@routines.route('/remove/<int:user_id>/<string:routine_name>')
class RemoveUserRoutine(Resource):
    def delete(self,user_id,routine_name):
        if request.method != "DELETE":
            return {
                "error": "This is a delete only route"
            }, 400

        elif User.find_user_by_id(user_id) is False:
            return {
                "error": "User with that id not found"
            },400

        else:
            current_user = User.find_user_by_id(user_id)

            try:
                if current_user.find_routine(routine_name) is False:
                    return {
                        "error": "No routine associated with that user"
                    }, 400

                else:
                    routine_to_delete = current_user.find_routine(routine_name)

                    print(routine_to_delete)

                    routine_to_delete.delete_routine()

                    return {
                        "success": "Deleted routine"
                    },200

            except Exception as e:
                return {
                    "error": "Error deleting routine please try again",
                    "details":str(e)
                },400

            
