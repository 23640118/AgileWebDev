# Test the login, logout, register functionality
from app import start_forum, db
from app.config import TestConfig
import unittest
from app.database import User, UserAction
from werkzeug.security import generate_password_hash

def write_db():
    # Add a test user
    user = User(username = 'test', email = 'test@t.com', password = generate_password_hash('password'))
    db.session.add(user)
    db.session.commit()

class TestAuth(unittest.TestCase):
    def setUp(self):
        testApp = start_forum(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        self.client = testApp.test_client()
        db.create_all()
        write_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_login_logout(self):
        # Test login
        response = self.client.post('/login', data=dict(
            email='test@t.com',
            password='password'), 
            follow_redirects=True)
        action = UserAction.query.filter_by(user_id = 1, action_type = 'LOGIN').first()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(action)
        # Test logout
        response = self.client.get('/logout', follow_redirects=True)
        action = UserAction.query.filter_by(user_id = 1, action_type = 'LOGOUT').first()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(action)
    
    def test_login_incorrect_password(self):
        # Attempt to log in with incorrect password
        response = self.client.post('/login', data=dict(
        email='test@t.com',
        password='incorrect_password'), 
        follow_redirects=True)
        # Check that login failed
        action = UserAction.query.filter_by(user_id = 1, action_type = 'LOGIN').first()
        self.assertIn(b'Login Failed: Please check email and password.', response.data)
        self.assertIsNone(action)

    def test_login_incorrect_email(self):
        # Attempt to log in with incorrect password
        response = self.client.post('/login', data=dict(
        email='Non_existence@user.com',
        password='password'), 
        follow_redirects=True)
        # Check that login failed
        self.assertIn(b'Login Failed: Please check email and password.', response.data)

    def test_signup(self):
        # Test sign up
        response = self.client.post('/signup', data=dict(
            email='test@test.com',
            username='test',
            password1='test'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        user = User.query.filter_by(email='test@test.com').first()
        action = UserAction.query.filter_by(user_id = user.user_id, action_type = 'REGISTER').first()
        self.assertIsNotNone(user)
        self.assertIsNotNone(action)

    def test_signup_existing_email(self):
        # Test sign up with email occupied by other user
        response = self.client.post('/signup', data=dict(
            email='test@t.com',
            username='test',
            password1='test'
        ), follow_redirects=True)
        self.assertIn(b'Email already exists.', response.data)


