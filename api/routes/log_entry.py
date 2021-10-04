from logging import log
from flask import (Blueprint, request)
from flask_restx import  Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from api.utils.auth_functions import verify_user

from api.models.models import User, Logs

log_entry = Namespace('logs', description="Endpoint for user routine exercises logs")


@log_entry.route('/')
class GetLogs(Resource):
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

@log_entry.route('/add/<string:routine_name>')
class LogEntry(Resource):
    @jwt_required()
    @verify_user
    def post(self,routine_name):
        '''Route for a user to submit log entries for completed exercises'''
        user_id = get_jwt_identity()

        current_user = User.find_user_by_id(user_id)

        # Now have the routine id
        user_routine = current_user.find_routine(routine_name)

        # Next obtain the exercise names and exercise ids of said routines

        exercises_in_routine = user_routine.get_exercises_in_routine()



        
        ## Route should take in an array of completed exercises with the required input: weight amount, reps, personal_routine id
        ## Assume request is an array 
        # {
        #     "data": [
        #         {
        #             "exercise_name": "Bicep Curl",
        #             "weight": 100,
        #             "reps": 8
        #         },
        #         ...
        #     ]
        # }
        workout_data = request.json["data"]

        for exercise in workout_data:
            # If submitted exercise name is in retrieved routine
            print(exercise)
            if any(retrieved_exercise["exercise_name"] == exercise["exercise_name"] for retrieved_exercise in exercises_in_routine):
                
                try:
                    log_input = Logs(weight=exercise["weight"], reps=exercise["reps"], routine_exercise_id=retrieved_exercise["routine_exercise_id"])
                    log_input.save_logs()
                except Exception as e:
                    return {
                        "error": "Error saving log please try again",
                        "details":str(e)
                    },400

        return {
            'success': 'Logs saved! Good Effort.'
        }, 200





        

       


