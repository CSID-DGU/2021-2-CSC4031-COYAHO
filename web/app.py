from flask import Flask, render_template, request, redirect
from models import db
import os
import requests
import yaml
import time
from models import Fcuser
from flask import session
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm
from werkzeug.utils import secure_filename
app = Flask(__name__)


@app.route('/')
def index():
    userid = session.get('userid', None)
    return render_template("index.html", userid=userid)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        fcuser = Fcuser()
        fcuser.userid = form.data.get('userid')

        fcuser.password = form.data.get('password')
        fcuser.grafana_ip = form.data.get('grafana_ip')

        print(fcuser.userid, fcuser.password)
        db.session.add(fcuser)
        db.session.commit()
        return render_template('index.html')
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['userid'] = form.data.get('userid')

        return redirect('/')
    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')


@app.route('/aws')
def aws():
    userid = session.get('userid', None)
    users = Fcuser.query.filter_by(userid=userid).all()
    return render_template('aws.html', users=users)


@app.route('/azure')
def azure():
    userid = session.get('userid', None)
    users = Fcuser.query.filter_by(userid=userid).all()
    return render_template('azure.html', users=users)


@app.route('/gcp')
def gcp():
    userid = session.get('userid', None)
    users = Fcuser.query.filter_by(userid=userid).all()
    return render_template('gcp.html', users=users)

# 파일 업로드 부분 template
@app.route('/upload')
def upload_file():
    return render_template('file_upload.html')

# 파일 업로드 수행
@app.route('/fileuploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == "POST":
        f = request.files['file']
        # 저장경로는 web/yaml폴더
        # f.save(secure_filename('./yaml/'+f.filename))
        f.save(secure_filename('./yaml/'+'recovery.yaml'))
        return 'file uploaded successfully'

# 파일 보내기
@app.route('/recovery')
def recovery():
    # 쿼리스트링으로 ip주소 받음
    target_namespace = request.args.get('namespace')  # 이 부분 추가작성 필요
    ip_address = request.args.get('ip_address')
    # 해당 아이피로 전송
    yaml_file_dir = './yaml/recovery.yaml'

    sample_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.1.2222.33 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }

    def send_request(target_URL=None, kind=None, yaml_data=None):
        requests.post(target_URL+'/'+kind +
                      f'/post?namespace={target_namespace}', json=yaml_data, headers=sample_headers)

    with open(os.path.join(os.path.dirname(__file__), yaml_file_dir)) as f:
        dep = list(yaml.safe_load_all(f))
        for i in range(len(dep)):
            time.sleep(1)
            kind = dep[i]['kind'].lower()
            send_request(target_URL=ip_address,
                         kind=kind, yaml_data=(dep[i]))

    return 'file sent successfully'


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

# 이 부분 추후 도커 패키징 시 kubernetes config에 따라 수정 필요
    app.run(host='127.0.0.1', port=5000, debug=True)
