from operator import index
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()          

class Fcuser(db.Model): 
    __tablename__ = 'fcuser'     
    userid = db.Column(db.String(32), primary_key = True, index = True)       #userid를 primarykey로 설정, 중복 아이디 제한
    password = db.Column(db.String(32), index = True)     
    grafana_ip = db.Column(db.String(8), index = True)
