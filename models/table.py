from flask_sqlalchemy import SQLAlchemy




db = SQLAlchemy()

class Table(db.Model):
    """ Protduc model """
    __tablename__ = "product"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    display_name = db.Column(db.String(100),nullable=False)
    
    
    def __str__(self):
        return self.name
