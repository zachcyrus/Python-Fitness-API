# Note currently testing using unittest just to compare againt pytest

import pytest
import json
from flask import jsonify

@pytest.fixture(scope='class')
def bearer_token(client):
    login_response = client.post(
            '/api/auth/login',
            data = json.dumps({
                "user_name": "Test_UserAB",
                "password":"testpass90"
            }),
            content_type='application/json'
        )

    print(login_response)

    token = json.loads(login_response.data.decode())["access_token"]

    return {
        'Authorization': 'Bearer {}'.format(token)
    }
    

class TestRoutineRoutes:
    def test_get_routine(self,client, bearer_token):
        '''Test that the GET self endpoint works, as well as a newly registered user has no routines assigned to them'''

        response = client.get(
            '/api/routines/self',
            headers = bearer_token
        )

        response_data = json.loads(response.data.decode()) 
        
        assert response.status_code == 200

        assert len(response_data["user_routine"]) == 0

        assert type(response_data["user_id"]) is int

    def test_add_routine(self,client,bearer_token):
        '''Test that the add endpoint works to add a routine to signed in user'''

        response = client.post(
            '/api/routines/add',
            headers = bearer_token,
            data = json.dumps({
                "routine_description": "Example routine description",
                "routine_name": "Example name of a routine"
            }),
            content_type='application/json'
        )
        
        response_data = json.loads(response.data.decode()) 

        assert response.status_code == 200

        assert 'routine' and 'success' in response_data
        
        assert type(response_data['routine']) is dict

    def test_add_exercise_to_routine(self,client,bearer_token):
        '''Test that a user can add an exercise to the newly created routine'''

        response = client.post(
            '/api/exercise/Example name of a routine',
            headers = bearer_token,
            data = json.dumps({
                "exercise_description": "Bicep curl description",
                "exercise_name": "Bicep Curl",
                "reps": 9
            }),
            content_type='application/json'
        )

        response_data = json.loads(response.data.decode()) 

        assert response.status_code == 200

        assert "exercise_name" and "exercise_description" and "reps" in response_data

        assert type(response_data["exercise_name"]) and type(response_data["exercise_description"]) is str

        assert response_data["exercise_name"] == "Bicep Curl"

        assert response_data['exercise_description'] == "Bicep curl description"

    def test_remove_routine(self, client, bearer_token):
        '''Test that a user is able to delete a routine'''

        retrieved_user_routines_response = client.get(
            '/api/routines/self',
            headers = bearer_token
        )

        retrieved_user_routines_data = json.loads(retrieved_user_routines_response.data.decode())

        total_user_routines = len(retrieved_user_routines_data["user_routine"])

        assert "Example name of a routine" in retrieved_user_routines_data["user_routine"]

        delete_user_routine_response = client.delete(
            '/api/routines/remove/Example name of a routine',
            headers = bearer_token
        )

        delete_user_routine_data = json.loads(delete_user_routine_response.data.decode())

        assert delete_user_routine_response.status_code == 200

        retrieved_user_routines_after_delete = client.get(
            '/api/routines/self',
            headers = bearer_token
        )

        user_routines_after_delete_data = json.loads(retrieved_user_routines_after_delete.data.decode())

        new_total_user_routines = len(user_routines_after_delete_data["user_routine"])

        assert total_user_routines == new_total_user_routines + 1

        





