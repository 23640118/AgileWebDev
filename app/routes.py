from flask import Blueprint, render_template, flash, redirect, url_for, request, Response
from flask_login import login_required, LoginManager, current_user
import random
from typing import cast
from . import db
from datetime import datetime, timedelta
from .database import *
from sqlalchemy import desc, and_


routes = Blueprint('routes', __name__)

def get_random_card(probability=None):
    from .database import Card
    rarity = ['common', 'rare', 'epic', 'legendary']
    if probability is None:
        probability = [0.60, 0.25, 0.14, 0.01]
    chosen_rarity = random.choices(rarity, weights=probability)[0]
    rarity_list = Card.query.filter_by(rarity = chosen_rarity).all()
    if not rarity_list:
        return None
    return random.choice(rarity_list)
  

@routes.route('/')
@routes.route('/index')
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)

@routes.route('/delete-post', methods=['POST'])
def delete():
    post_id = request.form.get('post_id')   # Post being completed
    u = current_user                        # User completing

    post = db.session.get(Post, post_id)

    # Confirm the both users have the required cards
    if not post:
        return Response(" Delete failed: post does not exist!", status = 400)
    
    # Mark trade as completed
    post.completed = True
    new_action = UserAction(action_type = 'DELETE_'+str(post.post_id), user_id = u.user_id)
    db.session.add(new_action) 
    db.session.commit()
    
    return "Post deleted!"

@routes.route('/update-post', methods=['POST'])
def trade():
    post_id = request.form.get('post_id')   # Post being completed
    u = current_user                        # User completing

    post = db.session.get(Post, post_id)
    trade_uid = post.owner_id
    trade_user = db.session.get(User, trade_uid)

    # Confirm the both users have the required cards
    for card in post.cards_traded:
        if card not in trade_user.cards:
            return Response(trade_user.username + " does not have the required card/s to complete this trade!", status = 400)
    
    for card in post.cards_wanted:
        if card not in u.cards:
            return Response("You don't have the required card/s to complete this trade!", status = 400)
    
    # Complete the trade
    for card in post.cards_traded:
            # Find the newest card instance for the trade_user
        newest_card = db.session.query(user_cards).filter(and_(user_cards.c.user_id == trade_uid, user_cards.c.card_id == card.card_id)).order_by(desc(user_cards.c.obtain_date)).first()
        if newest_card:
            db.session.execute(user_cards.delete().where(and_(user_cards.c.user_id == trade_uid, user_cards.c.card_id == card.card_id, user_cards.c.obtain_date == newest_card.obtain_date)))
        u.cards.append(card)

    for card in post.cards_wanted:
        newest_card = db.session.query(user_cards).filter(and_(user_cards.c.user_id == u.user_id, user_cards.c.card_id == card.card_id)).order_by(desc(user_cards.c.obtain_date)).first()
        if newest_card:
            db.session.execute(user_cards.delete().where(and_(user_cards.c.user_id == u.user_id, user_cards.c.card_id == card.card_id, user_cards.c.obtain_date == newest_card.obtain_date)))
        trade_user.cards.append(card)
        
    
    # Mark trade as completed
    post.completed = True
    new_action = UserAction(action_type = 'TRADE_'+str(post.post_id), user_id = u.user_id)
    db.session.add(new_action)

    db.session.commit()
    
    return "Congratulations! You've completed the trade!"

@routes.route('/post', methods=['GET','POST'])
def post():
    cards = Card.query.all()
    if request.method == 'POST':
        message = request.form.get('message')
        cards_traded = request.form.getlist('cards_traded')
        cards_wanted = request.form.getlist('cards_wanted')

        u = current_user
        new_post = Post(owner_id=u.user_id, message=message, completed=False)

        if len(cards_traded) == 0:
            flash('Select at least one card to trade', 'error')
            return redirect('/post')
        if len(cards_wanted) == 0:
            flash('Select at least one card you want in return', 'error')
            return redirect('/post')
        db.session.add(new_post)

        # Add traded cards to the post
        for card_id in cards_traded:
            card = db.session.get(Card, card_id)
            if card:
                new_post.cards_traded.append(card)
        
        # Add wanted cards to the post
        for card_id in cards_wanted:
            card = db.session.get(Card, card_id)
            if card:
                new_post.cards_wanted.append(card)

        db.session.flush()        
        new_action = UserAction(action_type = 'POST_'+str(new_post.post_id), user_id = u.user_id)
        db.session.add(new_action)
        db.session.commit()
        flash('Post Created!', 'success')
    return render_template('post.html', title='Make a post', cards=cards)

@routes.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first()
    cards = Card.query.all()
    n_posts = len(user.posts)
    n_cards = len(cards)
    n_owned = len(user.cards)
    return render_template('user.html', user=user, cards=cards, n_posts=n_posts, n_cards=n_cards, n_owned=n_owned)

@routes.route('/how_it_works')
def rules():
    return render_template('rules.html', title='How it works')

@login_required
@routes.route('/934910939049', methods=['GET','POST'])
def new_card():
    if current_user.user_id != 1:
        return render_template('rules.html', title='How it works')
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


@routes.route('/open_pack', methods=['POST'])
@login_required
def open_pack():
    user = cast(User, current_user)
    items = [get_random_card(probability=[0.60, 0.25, 0.14, 0.01]) for _ in range(5)]
    #Removes repeating cards
    unique_items = set(items)

    #Check for cards in database
    if None in unique_items:
        flash("An error occurred while opening the pack. Please contact administrators.", "error")
        return "None"
    
    for card in unique_items:
        user.cards.append(card)
    user.money += 1000
    new_action = UserAction(action_type = 'PACK_FREE', user_id = current_user.user_id)
    db.session.add(new_action)
    db.session.commit()
    print("ACTION ADDED")
    return render_template('open_pack.html', items=unique_items)

@routes.route('/open_pack_paid', methods=['POST'])
@login_required
def open_pack_paid():
    user = cast(User, current_user)
    if user.money < 1000:
        flash("Not enough money!")
        return "None"
    
    items = [get_random_card(probability=[0.40, 0.30, 0.20, 0.10]) for _ in range(5)]
    unique_items = set(items)

    user.money -= 1000

    if None in unique_items:
        flash("An error occurred while opening the pack. Please contact administrators.", "error")
        return "None"
    
    for card in unique_items:
        user.cards.append(card)

    new_action = UserAction(action_type = 'PACK_PAID', user_id = current_user.user_id)
    db.session.add(new_action)
    db.session.commit()
    print("ACTION ADDED")

    return render_template('open_pack.html', items=unique_items)
    
    
@routes.route('/inbox')
@login_required
def inbox():
    return render_template('inbox.html', title='Inbox')
