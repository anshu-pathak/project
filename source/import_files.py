from flask import Flask, request,Response
from flask_restful import Api, Resource, fields, marshal, marshal_with
from flask_api import FlaskAPI, status

from flask import redirect, render_template, url_for
import pandas as pd
import csv
import sqlite3
import xlrd

from models.table import Table

app = Flask(__name__)



import random

class CSVTable(Resource):
    """Create xlsx view API."""
    def post(self):
        data = request.form

        print("hello")
        file_name = request.files['file_name']
        strFileName = file_name.filename
        txt= strFileName[:-5]
        new_cdf = pd.read_excel(file_name)
        column_name = list(new_cdf.columns)
        print("==",column_name)
        table_name = txt
        create_sql = 'CREATE TABLE IF NOT EXISTS  ' + table_name + '(id_product_item INTEGER PRIMARY KEY,' \
            + ','.join(column_name) + ')'
        conn = sqlite3.connect('xlsx_database.db')
        c = conn.cursor()
        c.execute(create_sql)
        insert_sql = 'INSERT INTO ' + table_name + ' (' + ','.join(column_name) \
            + ') VALUES (' + ','.join(['?'] * len(column_name)) + ')'
        df = pd.DataFrame(new_cdf, columns=column_name)
        values = df.values.tolist()
        print("values",values)
        c.executemany(insert_sql, values)
        conn.commit()
        print("==",insert_sql)
        # save_operation.delay(create_sql,insert_sql,values)
        # save_operation.apply_async(args=[create_sql,insert_sql,values], countdown=60)

        return {"message": "Created successfully.","data":column_name}

class Hello(Resource):
    def get(self):
        return "hello"
    
    def post(self):
        files = request.files['file_name']
        print(files.filename)
        return "post"