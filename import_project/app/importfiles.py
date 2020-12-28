from flask import Flask, request,Response
from flask_restful import Api, Resource
import pandas as pd
import csv
import sqlite3
import xlrd
import numpy as np
# from models.model import ImportModel
from app import db
import stringcase

from sqlalchemy import create_engine

# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="padmin",
                               pw="anshu@1403",
                               db="import_files"))




class ImportExcel (Resource):
    """Create xlsx view API."""
    def post(self):
        
        file_name = request.files['file_name']
        strFileName = file_name.filename
        if strFileName.endswith(".csv") or strFileName.endswith(".xlsx") or strFileName.endswith(".xls"):

            txt= strFileName[:-5]
            
            table_name = correctName(txt)

            
            read = pd.read_excel(file_name)
            df = pd.DataFrame(read)

            lst = dict(df.dtypes)
            column1 = list(df.columns)
            table_colm = getType(lst)
            column_name = list([correctName(elem) for elem in column1])
        
            query  = "CREATE TABLE " + table_name + " (" + ", ".join(table_colm) + " )"
            
            db.session.execute(query)
            
            df.columns = column_name
            df.set_index(column_name[1], inplace=True)
            df.to_sql(table_name, con = engine, if_exists = 'append', chunksize = 1000)
        
            db.session.commit()
        
            return {"message": "Table Created successfully."}
        else :
            return {"message": "The file is not supported."}


def getType(text):
    namelist = []
    for key, val in text.items():
    
        if val =="int64":
            
            kry = stringcase.lowercase(key)
            kry = stringcase.snakecase(kry)
            # namelist.append(kry + " VARCHAR(50)")
            namelist.append(kry + " INT(60)")
        else:
            
            kry = stringcase.lowercase(key)
            kry = stringcase.snakecase(kry)
            namelist.append(kry + " VARCHAR(50)")

    print("the name list", namelist)
    return namelist
   


def correctName(txt):
    re = txt.strip().lower().replace(' ', '_')\
        .replace('(', '').replace('.', '_')\
            .replace(')', '').replace(',', '')\
                .replace('=','_').replace('-', '_')\
                    .replace('#', '').replace('__', '_')
    return re