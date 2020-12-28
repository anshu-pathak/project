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
        
        db.session.commit()
        return {"message": name +" table deleted successfully."}