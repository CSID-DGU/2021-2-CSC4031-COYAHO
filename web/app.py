from collections import UserDict
from flask import Flask, render_template, request, redirect, flash
import flask
from models import db
import os
import requests
import yaml
import time
from models import Fcuser
from flask import session
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm, UploadForm
from werkzeug.utils import secure_filename
import threading

app = Flask(__name__)


def get_url(prometheus_url):
    return prometheus_url


# prometheus_ip(prometheus ip), api_ip(flask api ip), status 서버 상태(정상 = True)
cloud_info = {'azure': {'prometheus_ip': '20.196.224.147', 'api_ip': '20.200.207.199', 'status': True},
              'aws': {'prometheus_ip': 'a790d6655f63c401c86fb7f46231d257-1084231655.us-west-2.elb.amazonaws.com', 'api_ip': 'ae50df8052d55419ab5df1bd7c72e9ef-1421424937.us-west-2.elb.amazonaws.com', 'status': True},
              'gcp': {'prometheus_ip': '34.121.224.0', 'api_ip': '34.134.51.2', 'status': True}}


def recovery_send():
    global cloud_info
    problem_flag = False

    # 검사
    for idx, csp in enumerate(cloud_info.keys()):
        if csp == 'azure':
            azure_connect_check()
        elif csp == 'aws':
            aws_connect_check()
        elif csp == 'gcp':
            gcp_connect_check()

        csp_stat = cloud_info[csp]
        # 조건문으로 클라우드에서 응답없음 확인
        if csp_stat['status'] is False:
            print(f'{csp} 클라우드에서 응답이 없습니다.')
            try:
                # 문제가 발생한 클라우드의 인덱스+1을 csp_to_recover로 지정
                csp_to_recover = list(cloud_info.keys())[idx+1]
            except:
                # 마지막 순번의 클라우드에 문제가 발생할 경우 첫 번째 클라우드로 지정
                csp_to_recover = list(cloud_info.keys())[0]
            # 문제가 발생한 클라우드를 cloud_info에서 삭제
            cloud_info.pop(csp)
            print(f'{csp} 클라우드가 모니터링 대상에서 제외되었습니다.')
            print(list(cloud_info.keys()))
            # problem_flag True로 변경
            problem_flag = True

            break
        else:
            print(f'{csp} 클라우드가 정상 작동하고 있습니다.')
    print(cloud_info)
    # problem_flag가 True이면 복구기능 수행
    if problem_flag:
        # csp_to_recover에 복구명령 전달
        print(cloud_info)
        print(f'{csp_to_recover} 클라우드에서 복구명령을 수행합니다')
        # 복구 수행
        print('복구가 완료되었습니다.')
    threading.Timer(60, recovery_send).start()


def azure_connect_check():
    global azure, cloud_info
    if azure:
        try:
            res = requests.get(
                "http://{}".format(get_url(cloud_info['azure']['prometheus_ip'])))
            print("azure "+str(res.status_code))
        except requests.Timeout:
            print("azure timeout")
            pass
        except requests.ConnectionError:
            print("azure connectionerror")
            # recovery(
            #    "http://{}".format(get_url(cloud_info['azure']['api_ip'])))
            cloud_info['azure']['status'] = False
            pass
        # finally:
        #    threading.Timer(20, azure_connect_check).start()


def aws_connect_check():
    global aws
    if aws:
        try:
            res = requests.get(
                "http://{}".format(get_url(cloud_info['aws']['prometheus_ip'])))
            print("aws "+str(res.status_code))

        except requests.Timeout:
            print("aws timeout")
            pass
        except requests.ConnectionError:
            print("aws connectionerror")
            # recovery("http://{}".format(get_url(cloud_info['aws']['api_ip'])))
            cloud_info['aws']['status'] = False
            pass
        # finally:
        #    threading.Timer(20, aws_connect_check).start()


def gcp_connect_check():
    global gcp
    if gcp:
        try:
            res = requests.get(
                "http://{}".format(get_url(cloud_info['gcp']['prometheus_ip'])))
            print("gcp "+str(res.status_code))

        except requests.Timeout:
            print("gcp timeout")
            pass
        except requests.ConnectionError:
            print("gcp connectionerror")
            # recovery("http://{}".format(get_url(cloud_info['gcp']['api_ip'])))
            cloud_info['gcp']['status'] = False
            pass
        # finally:
        #    threading.Timer(20, gcp_connect_check).start()


@app.route('/')
def index():
    userid = session.get('userid', None)
    return render_template("index.html", userid=userid)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = Fcuser.query.filter_by(userid=form.userid.data).first()

        if user:
            flash('이미 존재하는 아이디입니다.')

        else:
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
        user = Fcuser.query.filter_by(userid=form.userid.data).first()

        if user is not None and user.password == form.data.get('password'):
            session['userid'] = form.data.get('userid')
            return redirect('/')
        else:
            flash('아이디 또는 비밀번호가 일치하지 않습니다.')
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
    form = UploadForm()
    return render_template('file_upload.html', form=form)

# 파일 업로드 수행


@app.route('/fileuploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == "POST":
        f = request.files['file']
        # 저장경로는 web/yam/recovery.yaml
        savepath = '.\\web\\yaml\\recovery.yaml'
        f.save(savepath)
        return 'file uploaded successfully'

# 파일 보내기


def recovery(ip_address, **kwargs):
    # 쿼리스트링으로 ip주소 받음
    if 'target_namespace' not in kwargs.keys():
        target_namespace = 'default'
    else:
        target_namespace = kwargs['namespace']

    # 전송할 yaml파일 경로
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
    print('okay')
    return 'file sent successfully'


if __name__ == "__main__":
    basedir = os.path.abspath(os.path.dirname(__file__))
    dbfile = os.path.join(basedir, 'db.sqlite')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + dbfile
    app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'dev'

    csrf = CSRFProtect()
    csrf.init_app(app)

    db.init_app(app)
    db.app = app
    db.create_all()

    # azure_connect_check()
    # aws_connect_check()
    # gcp_connect_check()
    recovery_send()

# 도커 패키징
    # app.run(host='0.0.0.0', port=80, debug=True)
# localhost 테스트
    app.run(host='127.0.0.1', port=5000, debug=True)
