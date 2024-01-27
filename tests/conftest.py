import pytest

from unittest.mock import patch

from app.extensions.db import db
from app import create_app
from app.models import User
import bcrypt

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
    yield app.test_client()
    
@pytest.fixture
def client_activated_user(app):
    with app.app_context():
        plaintext_password = 'testpassword'
        hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt())

        user = User(
            email='test@email.com',
            username='user',
            password_hash=hashed_password.decode('utf-8'),
            activated=True,
            deactivated=False)
        
        db.session.add(user)
        db.session.commit()

        db.session.refresh(user)

    yield app.test_client(), user
