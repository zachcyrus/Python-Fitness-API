import pytest

from unittest import TestCase
from api import create_app, db as _db
import json

@pytest.fixture(scope='module')
def client():
    app = create_app(testing=True)
    
    with app.app_context():
        with app.test_client() as client:
            _db.create_all()
            yield client
            _db.session.remove()
            _db.drop_all()

class TestAuthRoute:
    def test_signup_route(self,client):
        '''Testing Signup Route for a new user'''

        signup_response =  client.post(
            '/api/auth/signup',
            data = json.dumps({
                "user_name": "Test_UserAB",
                "email": "test@gmail.com",
                "name": "Tester",
                "password":"testpass90"
            }),
            content_type='application/json'
        )
        assert signup_response.status_code == 200

        signup_response_data = json.loads(signup_response.data.decode())

        print(signup_response_data)
        
        assert signup_response_data["success"] == "New User signed up"

        assert type(signup_response_data["password"]) is str

        assert type(signup_response_data['user_id']) is int


    def test_login_route(self, client):
        '''Test login route for a registered user'''

        login_response = client.post(
            '/api/auth/login',
            data = json.dumps({
                "user_name": "Test_UserAB",
                "password":"testpass90"
            }),
            content_type='application/json'
        )

        assert login_response.status_code == 200

        