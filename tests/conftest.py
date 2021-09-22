import pytest
from api import create_app, db as _db


@pytest.fixture(scope="session")
def client():
    app = create_app(testing=True)
    
    with app.app_context():
        with app.test_client() as client:
            _db.create_all()
            yield client
            _db.session.remove()
            _db.drop_all()
