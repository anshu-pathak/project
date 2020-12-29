from flask import Flask, request,Response
from flask_restful import Api, Resource
import pandas as pd
import csv
import sqlite3
import xlrd
import numpy as np
from .model import ImportModel, ColumnTable
from app import db
import stringcase
import string
import random
import secrets


from sqlalchemy import create_engine

csprng = secrets.SystemRandom()

def random_string(len = 5, charsets = string.ascii_lowercase):
    return ''.join(csprng.choices(charsets, k = len))


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

        rf = request.form
        tbl =  rf['table_name']
        txt= strFileName[:-5]
        if tbl !="": 
           txt = tbl
            
        mimetype = file_name.content_type
        print("the type of the mimetype is ", mimetype)

        re_txt = random_string()
        table_name = correctName(txt)
        table_name = re_txt + "_"+ table_name

        print("the table name is ",table_name)
        if checkTblsExist(txt):
            return {"message": "Table already exist."} 
        else:    
            if strFileName.endswith(".xlsx") or strFileName.endswith(".xls"):

                read = pd.read_excel(file_name)
                df = pd.DataFrame(read)

                lst = dict(df.dtypes)
                column1 = list(df.columns)
                table_colm = getType(lst)
                column_name = list([correctName(elem) for elem in column1])

                

                ms_tbl= ImportModel(
                    name = table_name,
                    display_name = txt,
                )
                
                db.session.add(ms_tbl)
                db.session.commit()

                print("the ms_tbl" , ms_tbl)
                for k in column1:
                # for key in  column_name:

                    colms_tbl= ColumnTable(
                        tab_id= ms_tbl.id,
                        col_name = correctName(k),
                        col_display_name = k
                    )   
                    db.session.add(colms_tbl)
                    
                    print("the table is ", )    
                            

                query  = "CREATE TABLE " + table_name + " (" + ", ".join(table_colm) + " )"
                
                db.session.execute(query)
                
                df.columns = column_name
                df.set_index(column_name[1], inplace=True)
                df.to_sql(table_name, con = engine, if_exists = 'append', chunksize = 1000)
            
                db.session.commit()
                return {"message": "Table Created successfully."}
            elif strFileName.endswith(".csv"):
                txt= strFileName[:-5]
                

                # print("hello from csv", txt)
                # # print("the test is ", tt)
                
                read = pd.read_csv(file_name)
                df = pd.DataFrame(read)

                lst = dict(df.dtypes)
                
                column1 = list(df.columns)
                table_colm = getType(lst)
                column_name = list([correctName(elem) for elem in column1])
            
                ms_tbl= ImportModel(
                    name = table_name,
                    display_name = txt,
                )
                
                db.session.add(ms_tbl)
                db.session.commit()

                for k in column1:
                    colms_tbl= ColumnTable(
                        tab_id= ms_tbl.id,
                        col_name = correctName(k),
                        col_display_name = k
                    )   
                    db.session.add(colms_tbl)
            
                
                query  = "CREATE TABLE " + table_name + " (" + ", ".join(table_colm) + " )"
                
                db.session.execute(query)
                db.session.commit()
                
                df.columns = column_name
                df.set_index(column_name[1], inplace=True)
                df.to_sql(table_name, con = engine, if_exists = 'append', chunksize = 1000)
            

                return {"message": "Table Created successfully."}
            else :
                return {"message": "The file is not supported."}


def getType(text):
    namelist = []
    for key, val in text.items():
        if val =="int64":
            kry = correctName(key)
            namelist.append(kry + " INT")
        elif val == "datetime64[ns]" :
            kry = correctName(key)
            namelist.append(kry + " DATETIME")
        elif val == "float64" :
            kry = correctName(key)
            namelist.append(kry + " FLOAT")
        else:
            kry = correctName(key)
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






def checkTblsExist(tbl_name):
    print("the data is fsjdfkljasdfa", tbl_name)
    tble_exist = ImportModel.query.filter_by(display_name=tbl_name).first()
    if tble_exist:
        return True
    else:
        return False