from flask import Flask, request,Response
from flask_restful import Resource
import pandas as pd

from .model import ImportModel, ColumnTable
from app import db
import string
# import random
import secrets

# import mimetypes


from sqlalchemy import create_engine

# generate rendom string
csprng = secrets.SystemRandom()
def random_string(len = 5, charsets = string.ascii_lowercase):
    return ''.join(csprng.choices(charsets, k = len))


# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="padmin",
                               pw="anshu@1403",
                               db="import_files"))


class ImportFiles(Resource):
    '''
    import files from the user.
    '''
    def post(self):
                
        file_name = request.files['file_name']
        strFileName = file_name.filename

        splTxt = strFileName.split(".") 
        txt= splTxt[0]

        # ty =mimetypes.guess_extension(strFileName, strict=True)
        # ty =mimetypes.read(strFileName)
        # print("the name is print ",ty)
        # mimetype = file_name.content_type
        # print("the type of the mimetype is ", mimetype)

        re_txt = random_string()
        table_name = correctName(txt)
        table_name = re_txt + "_"+ table_name

        # print("the table name is ",table_name)
        if checkTblsExist(txt):
            return {"message": "Table already exist."} 
          
        if strFileName.endswith(".xlsx") or strFileName.endswith(".xls"):
            # for excel files 
            read = pd.read_excel(file_name)
            df = pd.DataFrame(read)
            # CreateTable(df, table_name, txt)
            rt = CreateTable(df, table_name, txt)
            return rt
            
        elif strFileName.endswith(".csv"):
            # for csv files
            read = pd.read_csv(file_name)
            df = pd.DataFrame(read)
            rt = CreateTable(df, table_name, txt)
            return rt
        else :
            return {"message": "The file is not supported."}


# get the table header types
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

    return namelist
   

# remove the special charecters
def correctName(txt):
    re = txt.strip().lower().replace(' ', '_')\
        .replace('(', '').replace('.', '_')\
            .replace(')', '').replace(',', '')\
                .replace('=','_').replace('-', '_')\
                    .replace('#', '').replace('__', '_')
    return re


# check the table is exist or not
def checkTblsExist(tbl_name):
    print("the data is fsjdfkljasdfa", tbl_name)
    tble_exist = ImportModel.query.filter_by(display_name=tbl_name).first()
    if tble_exist:
        return True
    else:
        return False


# create tabele in database
def CreateTable(df, table_name, txt):
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

class TrancateTable(Resource):
    def post(self):
        rf =request.form
        name= rf["table_name"]
        print("the table name is ", name)
        trancet = "TRUNCATE TABLE " +name

        db.session.execute(trancet)
        db.session.commit()
        return {"message": "Now the table is empty."}


