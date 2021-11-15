##데이터베이스와 관련된 코드

from operator import index
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()           #SQLAlchemy를 사용해 데이터베이스 저장

class Fcuser(db.Model): 
    __tablename__ = 'fcuser'   #테이블 이름 : fcuser
    #id = db.Column(db.Integer, primary_key = True, )   #id를 프라이머리키로 설정
    userid = db.Column(db.String(32), primary_key = True, index = True)       #이하 위와 동일
    password = db.Column(db.String(32), index = True)     #패스워드를 받아올 문자열길이 
    username = db.Column(db.String(8), index = True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)