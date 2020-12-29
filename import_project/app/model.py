from flask_sqlalchemy import SQLAlchemy
import datetime
from app import db , app

db = SQLAlchemy(app)
class ImportModel(db.Model):
    __tablename__ = "master_table"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(255), unique=True, nullable=False)


# CREATE TABLE master_table (
# id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
# name VARCHAR(100) NOT NULL UNIQUE,
# display_name VARCHAR(100) NOT NULL UNIQUE,
# )

class ColumnTable(db.Model):
    __tablename__ = "columns_tbl"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tab_id = db.Column(db.Integer(), nullable=False)
    col_name = db.Column(db.String(255), unique=False, nullable=False)
    col_display_name = db.Column(db.String(255), unique=False, nullable=False)



# CREATE TABLE columns_tbl (
# id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
# tab_id INT(6) NOT NULL,
# col_name VARCHAR(255) NOT NULL,
# col_display_name VARCHAR(255) NOT NULL
# )



