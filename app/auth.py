from flask import Blueprint, render_template, request, flash
from .database import User

#Routes for user account login/signup methods/pages only

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    
    return render_template('login.html', title='Log in')


@auth.route('/signup')
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        if password1 != password2:
            flash('')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        


    return render_template('signup.html', title='Sign up')