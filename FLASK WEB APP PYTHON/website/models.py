# this is where the database schema is defined

from . import db # importing the db object from the __init__.py file in this package directory
from flask_login import UserMixin #  this class is used to add user authentication to the app. it will be inherited by the User class
from sqlalchemy.sql import func #this class is used to get the current date and time

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True) # creating an id column that is the primary key
    data = db.Column(db.String(10000)) # creating a data column that can store up to 10000 characters
    date = db.Column(db.DateTime(timezone=True), default=func.now()) # creating a date column that stores the date and time the note was created
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) # creating a user_id column that is a foreign key to the id column in the user table. here "user" is lowercase because it is the name of the table not the class

class User(db.Model, UserMixin): # creating a User class that inherits from the db.Model class. this class will represent the users in the database
    id = db.Column(db.Integer, primary_key=True) # creating an id column that is the primary key
    email = db.Column(db.String(150), unique=True) # creating an email column that is unique
    password = db.Column(db.String(150)) # creating a password column
    first_name = db.Column(db.String(150)) # creating a first name column
    notes = db.relationship('Note') # each user can have multiple notes. here "Note" must be in capital N because it is the name of the class not the table

