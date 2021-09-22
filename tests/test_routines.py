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





