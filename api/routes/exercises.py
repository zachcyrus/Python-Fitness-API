# File for defining exercise API endpoint functions

from flask import (Blueprint, request)
from api.models.models import User, Routine_Exercises, Exercises
from flask_restx import  Resource, Namespace, fields
from flask_jwt_extended import jwt_required, get_jwt_identity


exercise = Namespace('Exercise', 'Exercises route for users')

exercise_model = exercise.model(
    "Added Exercise Model",
    {
        "exercise_name": fields.String(
            required=True,
            description='Name of exercise',
            help="Name cannot be blank"
        ),
        "exercise_description": fields.String(
            required=True,
            description='Description of exercise',
            help="Description cannot be empty"
        )
    }
)
# Route to add exercise to a particular routine

@exercise.route('/add/<string:routine_name>')
class AddExercise(Resource):
    @jwt_required()
    @exercise.expect(exercise_model)
    def post(self,routine_name):
        user_id = get_jwt_identity()

        # Error handling for requests not containing the required information

        if request.method != 'POST' or not(request.is_json):
            return {
                "error": "Request must be a POST method, and request body must contain JSON"
            }, 400

        elif ('exercise_name' or 'exercise_description') not in request.json:
            return {
                "error": "Request must contain exercise_name and exercise_description within the body"
            }, 400

        elif User.find_user_by_id(user_id) is False:
            return {
                "error": "User with that id doesn't exist"
            }, 400

        # Find routine with that name associated with that user

        else:

            current_user = User.find_user_by_id(user_id)

            current_user_routine = current_user.find_routine(routine_name)

            if current_user_routine is False:
                return {
                    "error": "Routine not found associated with that user_id"
                }, 400

            # Add exercise to exercise table

            try:
                exercise_to_add = Exercises(request.json)

                exercise_to_add.save_exercise()

                added_exercise_id = exercise_to_add.exercise_id

                # Now to save exercise to user_routine table

                new_routine_exercise = Routine_Exercises(reps=10,exercise_id=added_exercise_id,routine_id=current_user_routine.routine_id)

                new_routine_exercise.save_routine_exercises()

                return {
                    "routine_name": routine_name,
                    "exercise_name": exercise_to_add.exercise_name,
                    "reps": new_routine_exercise.reps

                },200



                
            except Exception as e:
                return {
                    "error": "Error creating routine table please try again",
                    "details":e
                },400
