import os
import tempfile

import pytest

from api import create_app

@pytest.fixture
def client():
    app = create_app(testing=True)
    
    with app.app_context():
        with app.test_client() as client:
            yield client

def test_user_route(client):
    rv =  client.get('/user/')
    assert rv.status_code == 200