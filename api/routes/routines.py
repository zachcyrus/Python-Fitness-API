# Route for defining routines endpoints

from flask import (Blueprint, request)
from api.models.models import Routines

bp = Blueprint('routines', __name__, url_prefix='/routines')

def add_routine(req):
    routine_dict = {
        "routine_name": req["routine_name"],
        "routine_description": req["routine_description"]
    }

    try:
        saved_routine = Routines(routine_dict)
        saved_routine.save_routine()
    except:
        return 'Error saving'

@bp.route('/', methods=["GET"])
def get_routines():
    # possibly return all user submitted routines
    try:
        return {
            "all_routines": Routines.get_all_routines()
        }, 200
    except:
        return {
            "error": "Error occurred retrieving data from DB"
        }, 400


@bp.route('/add', methods=["POST"])
def add_routines():
    if request.method != 'POST' or not(request.is_json):
        return {
            "error": "Request must be a POST method, and request must contain JSON"
        }, 400

    elif ('routine_description' or "routine_name") not in request.json:
        return {
            "error": "Request must contain a routine_description and routine_name"
        }, 400

    else:
        new_routine = request.json

        add_routine(new_routine)

        return {
            "success": new_routine["routine_name"] + " was successfully added!",
            "data": new_routine

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
