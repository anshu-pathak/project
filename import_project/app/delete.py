from flask import Flask, request,Response
from flask_restful import Api, Resource
import pymysql
from .model import ImportModel, ColumnTable
from app import db



class DeleteTable(Resource):
    
    def delete(self,id):
        imd = request.args
        lay = dict(request.args)
        payload = imd.to_dict(flat=False)

        import_table = ImportModel.query.get(id)

        if import_table is None:
            return {"message": 'NOT_EXISTS'}, 422
        else:
            tbl_name = import_table.name
            
            q = 'DELETE FROM master_table WHERE name ='+ "'" + tbl_name + "'"
            db.session.execute(q)
            db.session.commit()

            # delete columns
            qq = 'DELETE FROM columns_tbl WHERE tab_id =' + str(id) 
            db.session.execute(qq)
            db.session.commit()
            dropTable(tbl_name)
        return {"message": 'Deleted Successfully'}, 200



def dropTable(tb_name):
    query = "DROP TABLE IF EXISTS " + tb_name
    db.session.execute(query)
    db.session.commit()
    return



