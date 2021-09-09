# File for defining exercise API endpoint functions

# Routes to add: route to add an exercise to global list, route to remove an exercise 

# temp list of exercises

exercise_list = [
    "Bicep Curls",
    "Squats",
    "Bench Press"
]


from flask import (Blueprint, request)
from api.models.models import User, Routine_Exercises, Exercises

bp = Blueprint('exercise', __name__, url_prefix='/exercise')

@bp.route('/', methods=["GET"])
def get_exercises():
    return {"all_exercises":"testing"}


# Route to add exercise to a particular routine
@bp.route('/add/<int:user_id/<string:routine_name>', methods=["POST"])
def add_exercise_routine(user_id,routine_name):

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
