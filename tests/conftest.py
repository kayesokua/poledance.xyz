import pytest
from app.extensions.db import db
from app import create_app
from config import TestingConfig
from app.models import User

@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('config.TestingConfig')
    yield app

    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """
    A test client for the app.
    """
    yield app.test_client()