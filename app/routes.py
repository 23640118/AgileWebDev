from flask import Blueprint, render_template, request, flash, redirect, url_for, Response
from flask_login import login_required, current_user
from .database import Post, User, Card
from . import db
from datetime import datetime

routes = Blueprint('routes', __name__)



@routes.route('/')
@routes.route('/index')
def index():
    posts = Post.query.all()
    return render_template('index.html', title='Home', posts=posts)

@routes.route('/update-post', methods=['POST'])
def trade():
    post_id = request.form.get('post_id')   # Post being completed
    u = current_user                        # User completing

    post = Post.query.get(post_id)
    trade_uid = post.owner_id
    trade_user = User.query.get(trade_uid)

    # Confirm the both users have the required cards
    for card in post.cards_traded:
        if card not in trade_user.cards:
            return Response(trade_user.username + " does not have the required card/s to complete this trade!", status = 400)
    
    for card in post.cards_wanted:
        if card not in u.cards:
            return Response("You don't have the required card/s to complete this trade!", status = 400)
    
    # Complete the trade
    for card in post.cards_traded:
        trade_user.remove_card(card)
        u.add_card(card)

    for card in post.cards_wanted:
        trade_user.add_card(card)
        u.remove_card(card)
    
    # Mark trade as completed
    post.completed = True

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
        flash('Post Created!', 'success')
    return render_template('post.html', title='Make a post', cards=cards)


@routes.route('/how_it_works')
def rules():
    return render_template('rules.html', title='How it works')


@routes.route('/packs')
@login_required
def packs():
    return render_template('packs.html', title='Packs')

@routes.route('/inbox')
@login_required
def inbox():
    return render_template('inbox.html', title='Inbox')