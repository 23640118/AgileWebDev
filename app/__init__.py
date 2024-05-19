from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf import CSRFProtect

#initalise a database object
db = SQLAlchemy()

#initalise login manager object
login_manager = LoginManager()


#Starts forum
def start_forum(config):
    forum = Flask(__name__)
    csrf = CSRFProtect(forum)

    login_manager.init_app(forum)
    login_manager.login_view = 'auth.login'  # Redirects unauthorised users to login page
    login_manager.login_message_category = "error"

    #Configures the forum with key encrypting Cookies and Session data
    forum.config.from_object(config)
    
    db.init_app(forum)

    from .routes import routes
    from .auth import auth

    forum.register_blueprint(routes, url_prefix='/')
    forum.register_blueprint(auth, url_prefix='/')

    from . import database
    
    return forum
