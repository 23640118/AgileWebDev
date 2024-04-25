from flask import Blueprint, render_template
auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html', title='Log in')


@auth.route('/signup')
def signup():
    return render_template('signup.html', title='Sign up')