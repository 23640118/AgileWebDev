from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required
import random
from .database import Card

routes = Blueprint('routes', __name__)

def get_random_card():
    rarity = ['common', 'rare', 'epic', 'legendary']
    probability = [0.70, 0.15, 0.05, 0.01]
    chosen_rarity = random.choices(rarity, weights=probability)[0]
    rarity_list = Card.query.filter_by(rarity = chosen_rarity).all()
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
def open_pack():
    items = [get_random_card() for _ in range(5)]
    return render_template('open_pack.html', items=items)