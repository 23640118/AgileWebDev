from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#initalise a database object
db = SQLAlchemy()


#Starts forum
def start_forum():
    forum = Flask(__name__)
    #Configures the forum with key encrypting Cookies and Session data
    forum.config['SECRET_KEY'] = 'This Key Encrypts Cookies and Session Data Of User'
    forum.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  #sqlalchemy database is located at 'sqlite:///database.db'
    db.init_app(forum)

    from .routes import routes
    from .auth import auth

    forum.register_blueprint(routes, url_prefix='/')
    forum.register_blueprint(auth, url_prefix='/')

    from . import database
    #Create db file
    with forum.app_context():
        db.create_all()

    return forum
