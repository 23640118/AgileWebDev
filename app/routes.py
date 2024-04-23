from flask import render_template, flash, redirect, url_for
from app import app

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')

@app.route('/how_it_works')
def rules():
    return render_template('rules.html', title='How it works')

@app.route('/packs')
def packs():
    return render_template('packs.html', title='Packs')

@app.route('/login')
def login():
    return render_template('login.html', title='Log in')

@app.route('/signup')
def signup():
    return render_template('signup.html', title='Sign up')