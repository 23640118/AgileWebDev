from flask import Flask


#Starts forum
"""
!!!Please Read!!!: 
Code within start_forum() will execute twice within main.py
Please make sure that code added to start_forum() will run independently from the numbers of times the function is executed.
"""
def start_forum():
    forum = Flask(__name__)
    #Configures the forum with key encrypting Cookies and Session data
    forum.config['SECRET_KEY'] = 'This Key Encrypts Cookies and Session Data Of User'
    from .routes import routes
    from .auth import auth

    forum.register_blueprint(routes, url_prefix='/')
    forum.register_blueprint(auth, url_prefix='/')

    return forum
