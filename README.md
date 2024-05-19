# AgileWebDev

Purpose of Project/Application:
The forum is designed as a webpage for a marketpage to allow the obtaining, collection and trading of musical albums.
It should allow users of the forum to post their wanted trades to be seen across different users.
Users should be able to accept the post if they have the albums stated in the post and exchange the albums.


Summary of Architecture of the application:
The architecture of the application is based on 3 subdirectories of app. 
/static holds css stylesheet, fixed images and fixed javascript of the webpage.

/templates holds all python flask files which:
__init__.py initialises the flask application with security measures, database, login managers and routes assignment of the application. Executed in main.py

config.py contains security config functions that is initialised with the application including a administrator defined secret key for package encoding

auth.py and routes.py are both blueprints for the paths/routes of the flask application, processing user POST and GET.
auth.py is seperated from routes.py for management and security.

database.py defines the models and table of the database instance used to store application and user informations.

Running Tests:
Run all tests with command:
    python3 -m unittest discover tests


Launching the Application:
1. Set the key for environment variable "FLASK_SECRET_KEY".
2. Initialise database or on migration of the database run: "flask db upgrade" and "flask db migrate" 
3. Run the application with "flask run".
4. Signup, only the first signed up user is able to add new cards to forum (Administrator)
5. Append new cards/albums using '/934910939049' with administrator user


UWA ID and Github Username:
23640118 23640118
23380883 Si-yuY
23134051 harryprosser
23639838 liamdembUWA
