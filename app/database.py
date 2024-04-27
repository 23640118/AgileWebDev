from app import db
from flask_login import UserMixin
#SQLite
from sqlalchemy.sql import func

class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    message = db.Column(db.String(500))
    card_traded = db.Column(db.Integer, db.ForeignKey('card.card_id'))
    card_wanted = db.Column(db.Integer, db.ForeignKey('card.card_id'))
    completed = db.Column(db.Boolean)
    
class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20))
    money = db.Column(db.Integer)
    cards_owned = db.Column(db.String(100))          #all cards a user owns in a comma-separated list
    def get_id(self):
        return str(self.user_id)

class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    rarity = db.Column(db.String(9))                #'RARE', 'EPIC', 'LEGENDARY'
    name = db.Column(db.String(50), unique=True)
    url = db.Column(db.String(100))

class UserAction(db.Model):
    action_id = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.String(10))          #'POST_postID', 'EXCHANGE_postID", 'LOGIN', 'LOGOUT','REGISTER'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    