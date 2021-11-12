from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()          

class Fcuser(db.Model): 
    __tablename__ = 'fcuser'   
    id = db.Column(db.Integer, primary_key = True) 
    userid = db.Column(db.String(32))
    password = db.Column(db.String(64)) 
    aws_ip = db.Column(db.String(8))
    azure_ip = db.Column(db.String(8))
    gcp_ip = db.Column(db.String(8))