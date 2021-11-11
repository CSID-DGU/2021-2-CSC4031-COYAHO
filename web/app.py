from flask import Flask, render_template, request, redirect 
from models import db
import os
from models import Fcuser
app = Flask(__name__)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template("register.html")
    else:
        userid = request.form.get('userid')
        aws_ip = request.form.get('aws_ip')
        azure_ip = request.form.get('azure_ip')
        gcp_ip = request.form.get('gcp_ip')
        password = request.form.get('password')
        re_password = request.form.get('re_password')
        print(password) 

        if not (userid and aws_ip and azure_ip and gcp_ip and password and re_password) :
            return "모두 입력해주세요"
        elif password != re_password:
            return "비밀번호를 확인해주세요"
        else: 
            fcuser = Fcuser()         
            fcuser.password = password          
            fcuser.userid = userid
            fcuser.aws_ip = aws_ip
            fcuser.azure_ip = azure_ip  
            fcuser.gcp_ip = gcp_ip  
            db.session.add(fcuser)
            db.session.commit()
            return "회원가입 완료"

    # return redirect(url_for('/register'))

@app.route('/aws')
def aws():
    return render_template('aws.html')

@app.route('/azure')
def azure():
    return render_template('azure.html')

@app.route('/gcp')
def gcp():
    return render_template('gcp.html')

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))  
    dbfile = os.path.join(basedir, 'db.sqlite') 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True     
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   

    db.init_app(app) 
    db.app = app
    db.create_all()  

    app.run(host='127.0.0.1', port=5000, debug=True) 