# tests/test_auth.py

import pytest
from main import app
from extensions import db
from models.user import User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()

def test_register(client):
    response = client.post('/auth/register', data={
        'username': 'testuser',
        'email': 'test@example.com',
        'password': 'password',
        'confirm_password': 'password'
    }, follow_redirects=True)
    assert b'Your account has been created. Please log in.' in response.data

def test_login(client):
    with app.app_context():
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        db.session.add(user)
        db.session.commit()

    response = client.post('/auth/login', data={
        'email': 'test@example.com',
        'password': 'password',
        'remember': 'y'
    }, follow_redirects=True)
    assert b'You have been logged in.' in response.data

def test_invalid_login(client):
    response = client.post('/auth/login', data={
        'email': 'nonexistent@example.com',
        'password': 'wrongpassword'
    }, follow_redirects=True)
    assert b'Login unsuccessful. Please check email and password.' in response.data
