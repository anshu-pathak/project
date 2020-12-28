from flask import Flask, request, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api, Resource
from source.import_files import CSVTable, Hello
from models.table import db
from flask_mail import Mail, Message
from celery import Celery
import pdb 
app = Flask(__name__)


app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+://padmin:anshu@1403@localhost/import_files'
app.config['SECRET_KEY'] = 'f495b66803a6512d'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True


api = Api(app)
db.init_app(app)


# pdb.set_trace()

api.add_resource(Hello, '/')
api.add_resource(CSVTable, '/upload')

# pdb.addpost()

if __name__ == '__main__':
    app.debug = True
    app.run(debug=True, port=5000 )
