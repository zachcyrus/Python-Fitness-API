# Route for defining routines endpoints

from flask import (Blueprint, request)
import random

bp = Blueprint('routines', __name__, url_prefix='/routines')

user_routines = [
    {
        "id": 11,
        "routine_name": "Zach's PPL Routine",
        "exercises": [],
        "routine_id":342
    },
    {
        "id": 10,
        "routine_name": "GZCL Method Routine",
        "exercises": [],
        "routine_id":341
    }
]


@bp.route('/', methods=["GET"])
def get_routines():
    # possibly return all user submitted routines
    return {"all_routines": user_routines}


@bp.route('/add', methods=["POST"])
def add_routines():
    if request.method != 'POST' or not(request.is_json):
        return {
            "error": "Request must be a POST method, and request must contain JSON"
        }, 400

    elif ('id' or "routine_name" or "exercises") not in request.json:
        return {
            "error": "Request must contain a id, routine_name, and exercises"
        }, 400

    else:
        new_routine = request.json
        new_routine["routine_id"] = random.randint(343, 1103)
        user_routines.append(new_routine)
        return {
            "success": new_routine["routine_name"] + "was successfully added!",
            "data": user_routines

        }, 200


@bp.route('/remove/<int:routine_id>', methods=["DELETE"])
def remove_routine(routine_id):
    if request.method != "DELETE":
        return {
            "error": "This is a delete only route"
        }
    else:
        # have to loop through array of dicts
        for index, routine in enumerate(list(user_routines)):
            if routine_id == routine["routine_id"]:
                del user_routines[index]
                return {
                    "success": "Resource was successfully deleted"
                }, 200
        
        return {
            "error": "Routine id was not found"
        }, 400
