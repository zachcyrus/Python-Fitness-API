# Route for defining routines endpoints
# All routes tested and working as intended
from operator import add
from flask import (request)
from flask_restx import  Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
#from api.api import authorizations
from api.models.models import Routines, User_Routines, User

from api.routes.exercises import exercise_model

routines = Namespace('Routines', "Route for managing routines for different users", security="Bearer")

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

# Models for data to be expected by user as well as returned by API
model_for_returned_routine = routines.model(
    "Returned Routine Model",
    {
        "routine_id": fields.Integer,
        "routine_name":fields.String,
        "routine_description": fields.String
    }
)

all_user_routines_model = routines.model(
    "Retrieved User Routines",
    {
        "user_id": fields.Integer,
        "user_routine": fields.List(fields.Nested(model_for_returned_routine))
    }
)

user_routine_exercises_model = routines.model(
    "All exercises in a signed in users specific routine",
    {
        "routine_name": fields.String,
        "routine_description": fields.String,
        "exercises_list": fields.List(fields.Nested(exercise_model))
    }
)

routine_to_add_model = routines.model(
    "Expected data model for routine",
    {
        "routine_description": fields.String,
        "routine_name": fields.String
    }
)

success_added_routine_model = routines.model(
    "Data model for when a user successfully adds a routine",
    {
        "success": fields.String,
        "routine": fields.Nested(routine_to_add_model)
    }
)

successfully_deleted_routine_model = routines.model(
    "Response model for when a routine is deleted",
    {
        "success": fields.String
    }
)

@routines.route('/')
@routines.hide
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

# get routines for signed in user 
# works
# Protected route
@routines.route('/self')
class UserRoutines(Resource):
    @jwt_required()
    @routines.response(200, 'Success', all_user_routines_model)
    @routines.doc(security="Bearer")
    def get(self):
        '''Route to retrieve all routines of signed in user'''
        user_id = get_jwt_identity()

        print(type(user_id))

        current_user = User.find_user_by_id(user_id)

        if current_user is False:
            return {
                "error": "User with that ID not found"
            }, 400

        else:
            return {
                "user_id":current_user.user_id,
                "user_routine":current_user.get_routines()
            },200
        

# get specific routine with exercises for a particular user 
# Tested and works as intended
@routines.route('/<string:routine_name>')
class UserRoutineExercises(Resource): 
    @jwt_required()
    @routines.response(200, 'Success', user_routine_exercises_model)
    @routines.doc(security="Bearer")
    def get(self, routine_name):
        '''
        Route to retrieve all exercises of a specific routine
        '''
        user_id = get_jwt_identity()
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


# Route for addding a routine to a particular user
# Tested and works as intended
@routines.route('/add')
class AddUserRoutine(Resource):
    @jwt_required()
    @routines.expect(routine_to_add_model)
    @routines.response(200, 'Success', success_added_routine_model)
    @routines.doc(security="Bearer")
    def post(self):
        '''
        Route to add a routine to signed in user
        '''
        user_id = get_jwt_identity()
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


@routines.route('/remove/<string:routine_name>')
class RemoveUserRoutine(Resource):
    @jwt_required()
    @routines.response(200, 'Success', successfully_deleted_routine_model)
    @routines.doc(security="Bearer")
    def delete(self,routine_name):
        '''
        Route for deleting a user routine
        '''
        user_id = get_jwt_identity()
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

            
