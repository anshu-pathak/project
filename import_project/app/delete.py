from flask import Flask, request,Response
from flask_restful import Api, Resource
import pymysql
from app import db




class DeleteTable(Resource):
    
    def post(self):

        req = request.form
        print("the request form is ", )
        name = req['name']
        query = "DROP TABLE IF EXISTS " + name
        print("the name is ", query)
        
        db.session.execute(query)

        # tble_exist = ImportModel.query.filter_by(display_name=name).first()
        # sql = "SELECT id FROM master_table WHERE name = " + name

        db.session.execute(sql)
        
        db.session.commit()
        return {"message": name +" table deleted successfully."}