from app import db
from flask_login import UserMixin
#SQLite
from datetime import datetime
from sqlalchemy.orm import relationship
from hashlib import md5

# Table to user posts
class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now())
    message = db.Column(db.String(500))
    cards_traded = relationship('Card', secondary='post_cards_traded', backref='traded')
    cards_wanted = relationship('Card', secondary='post_cards_wanted', backref='posts_wanted')
    completed = db.Column(db.Boolean)

# Association table for cards traded in posts
post_cards_traded = db.Table('post_cards_traded',
    db.Column('post_id', db.Integer, db.ForeignKey('post.post_id')),
    db.Column('card_id', db.Integer, db.ForeignKey('card.card_id'))
)

# Association table for cards wanted in posts
post_cards_wanted = db.Table('post_cards_wanted',
    db.Column('post_id', db.Integer, db.ForeignKey('post.post_id')),
    db.Column('card_id', db.Integer, db.ForeignKey('card.card_id'))
)

#Table to store registered users 
class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20))
    money = db.Column(db.Integer)
    cards = db.relationship('Card', secondary='user_cards', backref=db.backref('users', lazy='dynamic'))
    posts = db.relationship('Post', backref='author', lazy=True)
    about = db.Column(db.String(500))
    
    #required for flask_login module
    def get_id(self):
        return str(self.user_id)
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
        

# Table that stores all the cards
class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    rarity = db.Column(db.String(9))                #'RARE', 'EPIC', 'LEGENDARY'
    name = db.Column(db.String(50), unique=True)
    artist = db.Column(db.String(50))
    year = db.Column(db.Integer)
    url = db.Column(db.String(100))

user_cards = db.Table('user_cards',
    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id')),
    db.Column('card_id', db.Integer, db.ForeignKey('card.card_id')),
    db.Column('obtain_date', db.DateTime(timezone=True), default=datetime.now())
)

# Table for logging user actions
class UserAction(db.Model):
    action_id = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.String(10))          #'POST_postID', 'TRADE_postID", 'LOGIN', 'LOGOUT','REGISTER','PACK_FREE','PACK_PAID'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now())
