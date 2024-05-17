from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, LoginManager, current_user
import random
from typing import cast
from . import db

routes = Blueprint('routes', __name__)

def get_random_card():
    from .database import Card
    rarity = ['common', 'rare', 'epic', 'legendary']
    probability = [0.60, 0.25, 0.14, 0.01]
    chosen_rarity = random.choices(rarity, weights=probability)[0]
    rarity_list = Card.query.filter_by(rarity = chosen_rarity).all()
    if not rarity_list:
        return None
    return random.choice(rarity_list)
  

@routes.route('/')
@routes.route('/index')
def index():
    return render_template('index.html', title='Home')


@routes.route('/how_it_works')
def rules():
    return render_template('rules.html', title='How it works')


@routes.route('/packs')
@login_required
def packs():
    return render_template('packs.html', title='Packs')

@routes.route('/open_pack')
@login_required
def open_pack():
    from .database import User, Card
    user = cast(User, current_user)
    items = [get_random_card() for _ in range(5)]

    if None in items:
        flash("An error occurred while opening the pack. Please try again.", "error")
        return "None"
    
    for card in items:
        user.cards.append(card)

    db.session.commit()
    return render_template('open_pack.html', items=items)
    