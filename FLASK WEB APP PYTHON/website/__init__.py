from flask import Flask # type: ignore
from flask_sqlalchemy import SQLAlchemy # type: ignore
from os import path
from flask_login import LoginManager

db = SQLAlchemy() # creating an instance of the SQLAlchemy class
DB_NAME = "database.db" # setting the name of the database

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///C:/Users/ben jazia/OneDrive/Documents/FLASK WEB APP PYTHON/website/database.db' # setting the URI of the database. this means that the database will be stored in a file called database.db in the root directory of the project
    db.init_app(app) # initializing the database with the app. this means that the database will be connected to the app

    from .views import views # importing the views blueprint from the views.py file
    from .auth import auth # importing the auth blueprint from the auth.py file

    app.register_blueprint(views, url_prefix='/') # registering the views blueprint with the app
    app.register_blueprint(auth, url_prefix='/') # registering the auth blueprint with the app. this prefix has to precede the route in the auth.py file. '/' means no prefix added


    from .models import User, Note
    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id)) # this function is used to reload the user object from the user ID stored in the session

    return app
import os
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Created Database!')

