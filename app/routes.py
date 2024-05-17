from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, LoginManager, current_user
import random
from typing import cast
from . import db
from datetime import datetime, timedelta
from .database import UserAction

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
    from .database import User, UserAction
    user = cast(User, current_user)
    # Get the time of the last free pack action
    last_free_pack_action = UserAction.query.filter_by(user_id=user.user_id, action_type='PACK_FREE').order_by(UserAction.date.desc()).first()
    if last_free_pack_action:
        time_since_last_pack = datetime.now() - last_free_pack_action.date
        if time_since_last_pack < timedelta(hours=24):
            #Calculate the remaining time
            remaining_time = timedelta(hours=24) - time_since_last_pack
        else:
            remaining_time = timedelta(seconds=0)
    else:
        remaining_time = timedelta(seconds=0)
    return render_template('packs.html', title='Packs', remaining_time=remaining_time.total_seconds())


@routes.route('/open_pack')
@login_required
def open_pack():
    from .database import User
    user = cast(User, current_user)
    items = [get_random_card() for _ in range(5)]

    #Check for cards in database
    if None in items:
        flash("An error occurred while opening the pack. Please contact administrators.", "error")
        return "None"
    
    for card in items:
        user.cards.append(card)
    new_action = UserAction(action_type = 'PACK_FREE', user_id = current_user.user_id)
    db.session.add(new_action)
    db.session.commit()
    return render_template('open_pack.html', items=items)
    
@routes.route('/inbox')
@login_required
def inbox():
    return render_template('inbox.html', title='Inbox')
