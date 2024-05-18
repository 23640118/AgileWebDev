# Test the post functionality
from app import start_forum, db
from app.config import TestConfig
import unittest
from app.database import User, Card
from werkzeug.security import generate_password_hash, check_password_hash

def write_db():
    user = User(username = 'test', email = 'test@t.com', password = generate_password_hash('asd'), money = 100)
    user2 = User(username = 'test', email = 'test1@t.com', password = generate_password_hash('asd'), money = 100)
    card = Card(rarity = 'legendary', name = "Blue", url = '/static/img/cards/Blue.png', artist = 'Jon', year = 1998)
    card2 = Card(rarity = 'epic', name = "Songs in the Key of Life", url = '/static/img/cards/Songs in the Key of Life.png', artist = 'Stevie', year = 1999)
    user.cards.append(card)
    user2.cards.append(card2)
    db.session.add_all([user, user2, card, card2])
    db.session.commit()


class BasicTest(unittest.TestCase):
    def setUp(self):
        testApp = start_forum(TestConfig)
        self.app_context = testApp.app_context()
        self.app_context.push()
        db.create_all()
        write_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
