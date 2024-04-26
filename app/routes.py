from flask import Blueprint, render_template, flash, redirect, url_for

routes = Blueprint('routes', __name__)



@routes.route('/')
@routes.route('/index')
def index():
    return render_template('index.html', title='Home')


@routes.route('/how_it_works')
def rules():
    return render_template('rules.html', title='How it works')


@routes.route('/packs')
def packs():
    return render_template('packs.html', title='Packs')