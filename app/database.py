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

class UserCard(db.Model):
    __tablename__ = 'user_cards'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    card_id = db.Column(db.Integer, db.ForeignKey('card.card_id'), primary_key=True)
    quantity = db.Column(db.Integer, default=1)
    user = relationship('User', back_populates='user_card_associations')
    card = relationship('Card', back_populates='card_user_associations')

#Table to store registered users 
class User(db.Model, UserMixin):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(10))
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(20))
    money = db.Column(db.Integer)
    user_card_associations = db.relationship('UserCard', back_populates='user', lazy='dynamic')
    posts = db.relationship('Post', backref='author', lazy=True)
    about = db.Column(db.String(500))

    #required for flask_login module
    def get_id(self):
        return str(self.user_id)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'
    
    @property
    def cards(self):
        return {uc.card: uc.quantity for uc in self.user_card_associations}

    def add_card(self, card, quantity=1):
        user_card = self.user_card_associations.filter_by(card_id=card.card_id).first()
        if user_card:
            if user_card.quantity != None:
                user_card.quantity += quantity
            else:
                user_card.quantity = 1
        else:
            user_card = UserCard(user_id=self.user_id, card_id=card.card_id, quantity=quantity)
            self.user_card_associations.append(user_card)
        db.session.add(user_card)
        db.session.commit()

    def remove_card(self, card, quantity=1):
        user_card = self.user_card_associations.filter_by(card_id=card.card_id).first()
        if user_card:
            if user_card.quantity > quantity:
                user_card.quantity -= quantity
            else:
                self.user_card_associations.remove(user_card)
                db.session.delete(user_card)
            db.session.commit()

# Table that stores all the cards
class Card(db.Model):
    card_id = db.Column(db.Integer, primary_key=True)
    rarity = db.Column(db.String(9))                #'RARE', 'EPIC', 'LEGENDARY'
    name = db.Column(db.String(50), unique=True)
    artist = db.Column(db.String(50))
    year = db.Column(db.Integer)
    url = db.Column(db.String(100))
    card_user_associations = db.relationship('UserCard', back_populates='card')

class UserAction(db.Model):
    action_id = db.Column(db.Integer, primary_key=True)
    action_type = db.Column(db.String(10))          #'POST_<postID>', 'TRADE_<postID>", 'LOGIN', 'LOGOUT','REGISTER','PACK_FREE','PACK_PAID', 'DELETE_<postID>'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    date = db.Column(db.DateTime(timezone=True), default=datetime.now())
