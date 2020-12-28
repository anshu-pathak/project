from flask_sqlalchemy import SQLAlchemy
import datetime
from app import db


class ImportModel(db.Model):
    __tablename__ = "master_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=False, nullable=False)
    display_name = db.Column(db.String(255), unique=False, nullable=False)
    data_type = db.Column(db.String(40), unique=False, nullable=True)
    
    col_meta = db.Column(db.JSON, nullable=True)




