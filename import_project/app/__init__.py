from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://padmin:anshu@1403@localhost/import_files'

db = SQLAlchemy(app)


api = Api(app)

def create_app():
    return app