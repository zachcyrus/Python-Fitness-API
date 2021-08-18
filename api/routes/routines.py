# Route for defining routines endpoints 

from flask import (Blueprint, request)

bp = Blueprint('routines', __name__, url_prefix='/routines')

user_routines = [
    {
        "id": 11,
        "routine_name": "Zach's PPL Routine",
        "exercises": []
    },
    {
        "id": 10,
        "routine_name": "GZCL Method Routine",
        "exercises": []
    }
]

@bp.route('/', methods=["GET"])
def get_routines():
    # possibly return all user submitted routines
    return {"all_routines":user_routines}

@bp.route('/add', methods=["POST"])
def add_routines():
    if request.method != 'POST' or not(request.is_json):
        return {
            "error": "Request must be a POST method, and request must be JSON"
        }, 400
    else:
        new_routine = request.json["routine"]
        