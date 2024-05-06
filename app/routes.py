from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_required
from .database import Post, User, Card
from . import db
from datetime import datetime

routes = Blueprint('routes', __name__)



@routes.route('/')
@routes.route('/index')
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)

@routes.route('/post', methods=['GET','POST'])
def post():
    cards = Card.query.all()
    if request.method == 'POST':
        message = request.form.get('message')
        cards_traded = request.form.getlist('cards_traded')
        cards_wanted = request.form.getlist('cards_wanted')

        u = db.session.get(User, 1)
        new_post = Post(owner_id=u.user_id, date=datetime.now(), message=message, completed=False)

        # Add traded cards to the post
        for card_id in cards_traded:
            card = Card.query.get(card_id)
            if card:
                new_post.cards_traded.append(card)
        
        # Add wanted cards to the post
        for card_id in cards_wanted:
            card = Card.query.get(card_id)
            if card:
                new_post.cards_wanted.append(card)

        db.session.add(new_post)
        db.session.commit()
    return render_template('post.html', title='Make a post', cards=cards)


@routes.route('/how_it_works')
def rules():
    return render_template('rules.html', title='How it works')

@routes.route('/934910939049', methods=['GET','POST'])
def new_card():
    if request.method == 'POST':
        name = request.form.get('name')
        rarity = request.form.get('rarity')
        url = "/static/img/cards/" + request.form.get('url') + ".png"

        new_card = Card(rarity=rarity, name=name, url=url)

        db.session.add(new_card)
        db.session.commit()
    return render_template('new_card.html', title='Mint a new card')



@routes.route('/packs')
@login_required
def packs():
    return render_template('packs.html', title='Packs')