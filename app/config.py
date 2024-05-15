from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY")

class DeploymentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"

class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory"
    TESTING = True