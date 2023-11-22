from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_app import app
import os


# Base directory for the database
database_dir = os.path.abspath(os.path.dirname(__file__))

# Configure database and marshmallow
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(database_dir, 'db.sqlite')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
marshmallow = Marshmallow(app)

# Objects that should be initially added when the database is created
database_init=[]

# Create the database if it does not exist and add all initial objects
def create_database():
    with app.app_context():
        db.create_all()
        for item in database_init:
            db.session.add(item)
        db.session.commit()

