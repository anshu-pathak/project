from flask import Flask,request
from flask_sqlalchemy import SQLAlchemy
# import pymysql
from app import api, create_app

from app.importfiles import ImportExcel
from app.delete import DeleteTable


api.add_resource(ImportExcel, '/upload')
api.add_resource(DeleteTable, '/delete')

app = create_app()

if __name__ == '__main__':
    app.debug = True
    app.run(port=7000)
