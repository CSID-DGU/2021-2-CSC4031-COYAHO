from logging import debug
from flask import Flask, render_template, request, redirect #render_template으로 html파일 렌더링
from models import db
import os
from models import Fcuser
app = Flask(__name__)

@app.route('/', methods = ['POST', 'GET'])
# def index():
#     tasks = Fcuser.query.order_by(Fcuser.userid).all()
#     return render_template('testpage.html', tasks = tasks)

def index():
    target = Fcuser.query.filter_by(userid='aws').all()
    return render_template('testpage.html', target = target)

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))  # database 경로를 절대경로로 설정함
    dbfile = os.path.join(basedir, 'db.sqlite') # 데이터베이스 이름과 경로
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True     # 사용자에게 원하는 정보를 전달완료했을때가 TEARDOWN, 그 순간마다 COMMIT을 하도록 한다.라는 설정
    #여러가지 쌓아져있던 동작들을 Commit을 해주어야 데이터베이스에 반영됨. 이러한 단위들은 트렌젝션이라고함.
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # True하면 warrnig메시지 유발, 

    db.init_app(app) #초기화 후 db.app에 app으로 명시적으로 넣어줌
    db.app = app
    db.create_all()   # 이 명령이 있어야 생성됨. DB가


    app.run(host='127.0.0.1', port=5000, debug=True) 