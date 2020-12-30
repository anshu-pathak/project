from app import db
from flask import Flask, request, Response, render_template
from flask_restful import Resource  
from .importfiles import engine

class getTable(Resource):
    def get(self):
        engine.execute('SELECT * FROM master_table')

        data = engine.fetchall()

        print("the data is ", data )
        return render_template('example.html', output_data = data)
        # return render_template('test.html', user=user_details)
