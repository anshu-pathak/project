from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate # importing our latest dependency

# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/learn-flask-migrate'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://padmin:anshu@1403@localhost/import_files'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy()
# Migrate(app, db) # this exposes some new flask terminal commands to us!

class Student(db.Model):

    __tablename__ = "students" # table name will default to name of the model

    # Create the three columns for our table
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)

    # define what each instance or row in the DB will have (id is taken care of for you)
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    # this is not essential, but a valuable method to overwrite as this is what we will see when we print out an instance in a REPL.
    def __repr__(self):
        return f"The student's name is {self.first_name} {self.last_name}"