from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path

#initalise a database object
db = SQLAlchemy()
DB_NAME = "database.db"


#Starts forum
def start_forum():
    forum = Flask(__name__)
    #Configures the forum with key encrypting Cookies and Session data
    forum.config['SECRET_KEY'] = 'This Key Encrypts Cookies and Session Data Of User'
    forum.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'  #sqlalchemy database is located at f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .routes import routes
    from .auth import auth

    forum.register_blueprint(routes, url_prefix='/')
    forum.register_blueprint(auth, url_prefix='/')

    from . import database

    create_database(app)

    return forum

def create_database(app):
    if not path.exists('app/' + DB_NAME):
        db.create_all(app=app)
