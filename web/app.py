from collections import UserDict
from flask import Flask, render_template, request, redirect, flash
import flask
from models import db
import os
from models import Fcuser
from flask import session
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm
app = Flask(__name__)

@app.route('/')
def index():
    userid = session.get('userid', None)
    return render_template("index.html", userid=userid)

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Fcuser.query.filter_by(userid = form.userid.data).first()

        if user:
            flash('이미 존재하는 아이디입니다.')

        else:
            fcuser = Fcuser()
            fcuser.userid = form.data.get('userid')

            fcuser.password = form.data.get('password')
            fcuser.grafana_ip = form.data.get('grafana_ip')

            print(fcuser.userid,fcuser.password)  
            db.session.add(fcuser)  
            db.session.commit() 
            return render_template('index.html')
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])  
def login():  
    form = LoginForm() 
    if form.validate_on_submit():

        user = Fcuser.query.filter_by(userid=form.userid.data).first()

        if user is not None and user.password == form.data.get('password'):
            session['userid'] = form.data.get('userid') 
            return redirect('/')
        else:
            flash('아이디 또는 비밀번호가 일치하지 않습니다.')
            
    return render_template('login.html', form=form)

@app.route('/logout',methods=['GET'])
def logout():
    session.pop('userid',None)
    return redirect('/')

@app.route('/aws')
def aws():
    userid = session.get('userid', None)
    users = Fcuser.query.filter_by(userid=userid).all()
    return render_template('aws.html', users = users)

@app.route('/azure')
def azure():
    userid = session.get('userid', None)
    users = Fcuser.query.filter_by(userid=userid).all()
    return render_template('azure.html', users = users)

@app.route('/gcp')
def gcp():
    userid = session.get('userid', None)
    users = Fcuser.query.filter_by(userid=userid).all()
    return render_template('gcp.html', users = users)

if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))  
    dbfile = os.path.join(basedir, 'db.sqlite') 
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True     
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'wcsfeufhwiquehfdx'

    csrf = CSRFProtect()
    csrf.init_app(app)   

    db.init_app(app) 
    db.app = app
    db.create_all()  

    app.run(host='127.0.0.1', port=5000, debug=True) 