from flask import Blueprint, render_template, request, flash, redirect, url_for
from .database import User, UserAction
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user, LoginManager

#Routes for user account login/signup methods/pages only

auth = Blueprint('auth', __name__)

from . import login_manager

@login_manager.user_loader
def load_user(user_id):
    user_id = User.query.get(user_id)
    if user_id: return user_id
    return None

@auth.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    new_action = UserAction(action_type = 'LOGOUT', user_id = current_user.user_id)
    db.session.add(new_action)
    db.session.commit()
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user,remember=True)
                new_action = UserAction(action_type = 'LOGIN', user_id = current_user.user_id)
                db.session.add(new_action)
                db.session.commit()
                return redirect(url_for('routes.packs'))
            else:
                flash('Username and Password Does not Match.', category='error')
        else:
            flash('Username and Password Does not Match.', category='error')
    return render_template('login.html', title='Log in')


@auth.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')

        user = User.query.filter_by(email=email).first()
        if user != None:
            flash('Email already exists.', category='error')
        else:
            new_user = User(email=email,username=username, password=generate_password_hash(password1, method='pbkdf2:sha256'), money=0)
            db.session.add(new_user)
            new_action = UserAction(action_type = 'REGISTER', user_id = db.session.query(User).count())
            db.session.add(new_action)
            db.session.commit()
            flash('Signup Success! Account Created!', category = 'success')
            return render_template('signup.html', title='Sign up')
    return render_template('signup.html', title='Sign up')

