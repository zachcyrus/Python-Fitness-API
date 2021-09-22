# Note currently testing using unittest just to compare againt pytest

import pytest
import json

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
    def test_self_endpoint(self,client, bearer_token):
        '''Test that the GET self endpoint works, as well as a newly registered user has no routines assigned to them'''

        response = client.get(
            '/api/routines/self',
            headers = bearer_token
        )

        response_data = json.loads(response.data.decode()) 
        
        assert response.status_code == 200

        assert len(response_data["user_routine"]) == 0

        assert type(response_data["user_id"]) is int


