# Route for defining routines endpoints

from operator import add
from flask import (Blueprint, request)
from api.models.models import Routines, User_Routines, User

bp = Blueprint('routines', __name__, url_prefix='/routines')

def add_routine(req):
    routine_dict = {
        "routine_name": req["routine_name"],
        "routine_description": req["routine_description"]
    }

    try:
        saved_routine = Routines(routine_dict)
        current_routine_id = saved_routine.save_routine()
        return current_routine_id
    except:
        return 'Error saving'

@bp.route('/', methods=["GET"])
def get_routines():
    # possibly return all user submitted routines
    print(Routines.get_all_routines())
    try:
        return {
            "all_routines": Routines.get_all_routines()
        }, 200
    except:
        return {
            "error": "Error occurred retrieving data from DB"
        }, 400

#get routines for specific user 
@bp.route('/<int:user_id>', methods=["GET"])
def get_user_routines(user_id):
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

#Route for addding a routine to a particular user
@bp.route('/add/<int:user_id>', methods=["POST"])
def add_user_routine(user_id):
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

        # Make a routine table 

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
                "details":e
            },400


@bp.route('/remove/<int:user_id>/<string:routine_name>', methods=["DELETE"])
def remove_routine(user_id,routine_name):
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

        return {
            "user":user_id,
            "user_routine":current_user.routines
        },200
