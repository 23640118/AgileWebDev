from flask import Flask


#Starts forum
def start_forum():
    forum = Flask(__name__)
    #Configures the forum with key encrypting Cookies and Session data
    forum.config['SECRET_KEY'] = 'This Key Encrypts Cookies and Session Data Of User'
    from .routes import routes
    from .auth import auth
    
    #This links routes.py and auth.py with the forum application
    forum.register_blueprint(routes, url_prefix='/')
    forum.register_blueprint(auth, url_prefix='/')

    return forum