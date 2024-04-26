from flask import Blueprint, render_template, request

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



    return render_template('signup.html', title='Sign up')