# File for defining exercise API endpoint functions

# Routes to add: route to add an exercise to global list, route to remove an exercise 

# temp list of exercises

exercise_list = [
    "Bicep Curls",
    "Squats",
    "Bench Press"
]


from flask import (Blueprint, request)

bp = Blueprint('exercise', __name__, url_prefix='/exercise')

@bp.route('/', methods=["GET"])
def get_exercises():
    # flask apparently returns python dicts as json automatically
    return {"all_exercises":exercise_list}

@bp.route('/add', methods=["POST"])
def add_exercise():


    '''

    Format for data that should be posted
    {
        exercise_name: "Sample"
    }

    '''


    if request.method != 'POST' or not(request.is_json):
        return {
            "error": "Request must be a POST method, and request must be JSON"
        }, 400
    else:
        new_exercise = request.json["exercise_name"]
        exercise_list.append(new_exercise)

        return {
            "success": new_exercise + " was successfully added",
            "exercise_list":exercise_list
        }, 200
