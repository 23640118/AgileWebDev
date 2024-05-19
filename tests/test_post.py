# Test the post functionality
from app import start_forum, db
from app.config import TestConfig
import unittest
from app.database import User, Card, UserAction, Post
from werkzeug.security import generate_password_hash

def write_db():
    # Create user 1 with card 1
    user = User(username = 'test', email = 'test@t.com', password = generate_password_hash('pwd'), money = 100)
    card = Card(rarity = 'legendary', name = "Blue", url = '/static/img/cards/Blue.png', artist = 'Jon', year = 1998)
    # Create user 2 with card 2
    user2 = User(username = 'test', email = 'test1@t.com', password = generate_password_hash('pwd'), money = 100)
    card2 = Card(rarity = 'epic', name = "Song1", url = '/static/img/cards/Blue.png', artist = 'Stevie', year = 1999)
    # Create a card no one owns
    card3 = Card(rarity = 'common', name = "Song2", url = '/static/img/cards/Blue.png', artist = 'Artist', year = 1999)
    # Create a post by user 2 where user 1 can trade
    post = Post(owner_id = 2, completed = False)
    post.cards_traded.append(card2)
    post.cards_wanted.append(card)
    # Create a post by user 2 where user 1 can't trade
    post2 = Post(owner_id = 2, completed = False)
    post2.cards_traded.append(card2)
    post2.cards_wanted.append(card3)
    # Create a post by user 2 where user 2 can't trade
    post3 = Post(owner_id = 2, completed = False)
    post3.cards_traded.append(card3)
    post3.cards_wanted.append(card)
    # Add data to database
    db.session.add_all([user, user2, card, card2, card3, post, post2, post3])
    db.session.commit()
    user.add_card(card)
    user2.add_card(card2)
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
    
    def test_post_and_delete(self):
        # Test create post
        response = self.client.post('/post', data=dict(
            message = '',
            cards_traded = [1],
            cards_wanted = [2]), 
            follow_redirects=True)
        # Check the existence of Post 4
        post = Post.query.filter_by(owner_id = 1, completed = False).first()
        action = UserAction.query.filter_by(user_id = 1, action_type = 'POST_4').first()
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(action)
        self.assertIsNotNone(post)

        # Test delete the post
        response = self.client.post('/delete-post', data=dict(
            post_id = 4), 
            follow_redirects=True)
        self.assertIn(b"Post deleted!", response.data)
        # Check post 4 is completed
        post = Post.query.filter_by(owner_id = 1, completed = True).first()
        action = UserAction.query.filter_by(user_id = 1, action_type = 'DELETE_4').first()
        self.assertIsNotNone(action)
        self.assertIsNotNone(post)
    
    def test_bad_post(self):
        # Test create post with no trade card selected
        response = self.client.post('/post', data=dict(
            message = '',
            cards_wanted = [2]), 
            follow_redirects=True)
        # Check post was not created
        post = Post.query.filter_by(owner_id = 1, completed = False).first()
        self.assertIn(b'Select at least one card to trade', response.data)
        self.assertIsNone(post)

    def test_bad_post2(self):
        # Test create post with no wanted card selected
        response = self.client.post('/post', data=dict(
            message = '',
            cards_traded = [1]), 
            follow_redirects=True)
        # Check post was not created
        post = Post.query.filter_by(owner_id = 1, completed = False).first()
        self.assertIn(b'Select at least one card you want in return', response.data)
        self.assertIsNone(post)
    
    def test_trade(self):
        # Test trade with user 2 in post 1
        response = self.client.post('/update-post', data=dict(
            post_id=1),
            follow_redirects=True)
        # Check the post is set as completed
        post = Post.query.filter_by(post_id = 1, completed = True).first()
        action = UserAction.query.filter_by(user_id = 1, action_type = 'TRADE_1').first()
        self.assertIsNotNone(post)
        self.assertIsNotNone(action)
        self.assertIn(b"Congratulations! You've completed the trade!", response.data)

    def test_bad_trade(self):
        # Test trade with user 2 in post 2
        response = self.client.post('/update-post', data=dict(
            post_id=2),
            follow_redirects=True)
        # Check the post is not set as completed
        post = Post.query.filter_by(post_id = 2, completed = False).first()
        action = UserAction.query.filter_by(user_id = 1, action_type = 'TRADE_2').first()
        self.assertIsNotNone(post)
        self.assertIsNone(action)
        self.assertIn(b"You don't have the required card/s to complete this trade!", response.data)
        self.assertEqual(response.status_code, 400)

    def test_bad_trade2(self):
        # Test trade with user 2 in post 3
        response = self.client.post('/update-post', data=dict(
            post_id=3),
            follow_redirects=True)
        # Check the post is not set as completed
        post = Post.query.filter_by(post_id = 3, completed = False).first()
        action = UserAction.query.filter_by(user_id = 1, action_type = 'TRADE_3').first()
        self.assertIsNotNone(post)
        self.assertIsNone(action)
        self.assertIn(b" does not have the required card/s to complete this trade!", response.data)
        self.assertEqual(response.status_code, 400)
