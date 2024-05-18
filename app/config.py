from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
 

class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"
    SECRET_KEY = 'secret'
    TESTING = True