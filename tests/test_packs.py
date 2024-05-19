# Test the pack functionality
from app import start_forum, db
from app.config import TestConfig
import unittest
from app.database import User, Card, UserAction
from werkzeug.security import generate_password_hash
from unittest.mock import patch

def write_db():
    user = User(username = 'test', email = 'test@t.com', password = generate_password_hash('pwd'), money = 100)
    card1 = Card(rarity = 'epic', name = "1", url = '/static/img/cards/Blue.png', artist = 'Jon', year = 1998)
    card2 = Card(rarity = 'common', name = "2", url = '/static/img/cards/Blue.png', artist = 'Jon', year = 1998)
    card3 = Card(rarity = 'rare', name = "3", url = '/static/img/cards/Blue.png', artist = 'Jon', year = 1998)
    card4 = Card(rarity = 'common', name = "4", url = '/static/img/cards/Blue.png', artist = 'Jon', year = 1998)
    card5 = Card(rarity = 'legendary', name = "5", url = '/static/img/cards/Blue.png', artist = 'Jon', year = 1998)
    db.session.add_all([user, card1, card2, card3, card4, card5])
    db.session.commit()

def login(client):
    # Login as user 1
    client.post('/login', data=dict(
        email='test@t.com',
        password='pwd'), 
        follow_redirects=True)

class BasicTest(unittest.TestCase):
    def setUp(self):
        testApp = start_forum(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        self.client = testApp.test_client()
        db.create_all()
        write_db()
        login(self.client)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_free_pack(self):
        # Test remaining time is 0 for new users
        with patch('app.routes.render_template') as mock:
            response = self.client.get('/packs', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            # Check that render_template was called with remaining_time as an argument
            args, kwargs = mock.call_args
            remaining_time = kwargs['remaining_time']
            self.assertEqual(remaining_time, 0)

    def test_open_pack(self):
        # Open free pack
        response = self.client.get('/open_pack', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        action = UserAction.query.filter_by(user_id = 1, action_type = 'PACK_FREE').first()
        user = User.query.filter_by(user_id = 1).first()
        # Check user has gained card/s
        number_of_cards = len(user.cards)
        self.assertTrue(number_of_cards>0)
        self.assertIsNotNone(action)

    def test_open_pack_during_count_down(self):
        # Try to open free cards while there is time remaining\
        action = UserAction(user_id = 1, action_type = 'PACK_FREE')
        db.session.add(action)
        db.session.commit()
        response = self.client.get('/open_pack', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        action2 = UserAction.query.filter_by(user_id = 1, action_type = 'PACK_FREE').order_by(UserAction.date.desc()).first()
        user = User.query.filter_by(user_id = 1).first()
        # Check no new free pack in userAction table
        self.assertTrue(action.action_id == action2.action_id)
        # Check user gain no cards
        self.assertTrue(len(user.cards) == 0)
