from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

#initalise a database object
db = SQLAlchemy()

#initalise login manager object
login_manager = LoginManager()

migrate = Migrate()

#Starts forum
def start_forum():
    forum = Flask(__name__)

    login_manager.init_app(forum)
    login_manager.login_view = 'auth.login'  # Redirects unauthorised users to login page
    #login_manager.login_message_category = "error"

    #Configures the forum with key encrypting Cookies and Session data
    forum.config['SECRET_KEY'] = 'This Key Encrypts Cookies and Session Data Of User'
    forum.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  #sqlalchemy database is located at 'sqlite:///database.db'
    forum.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(forum)
    migrate.init_app(forum, db)

    from .routes import routes
    from .auth import auth

    forum.register_blueprint(routes, url_prefix='/')
    forum.register_blueprint(auth, url_prefix='/')

    from . import database
    
    return forum
