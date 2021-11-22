from collections import UserDict
from flask import Flask, render_template, request, redirect, flash, session
from models import db
import os
import requests
import yaml
import time
from models import Fcuser
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm, UploadForm, GrafanaForm
from werkzeug.utils import secure_filename
import threading

app = Flask(__name__)

prometheus = {'azure': '20.196.224.147', 'gcp': '34.121.224.0',
              'aws': 'a790d6655f63c401c86fb7f46231d257-1084231655.us-west-2.elb.amazonaws.com'}
flask_api = {'azure': '20.200.207.199', 'gcp': '34.134.51.2',
             'aws': 'ae50df8052d55419ab5df1bd7c72e9ef-1421424937.us-west-2.elb.amazonaws.com'}
# 'azure': '20.196.224.147'
# 'azure': '20.200.207.199'

def get_url(prometheus_url):
    return prometheus_url

# 각 클라우드 connection check하는 코드
# connect 될 때 True, 안되면 False
aws = True
azure = True
gcp = True

def azure_connect_check():
    global azure
    if azure:
        try:
            res = requests.get("http://"+get_url(prometheus['azure']))
            print("azure "+str(res.status_code))
        except requests.Timeout:
            print("azure timeout")
            pass
        except requests.ConnectionError:
            print("azure connectionerror")
            recovery("http://"+flask_api['azure'])
            azure = False
            pass
        finally:
            threading.Timer(20, azure_connect_check).start()
            
def aws_connect_check():
    global aws
    if aws:
        try:
            res = requests.get("http://"+get_url(prometheus['aws']))
            print("aws "+str(res.status_code))

        except requests.Timeout:
            print("aws timeout")
            pass
        except requests.ConnectionError:
            print("aws connectionerror")
            recovery("http://"+flask_api['aws'])
            aws = False
            pass
        finally:
            threading.Timer(20, aws_connect_check).start()


def gcp_connect_check():
    global gcp
    if gcp:
        try:
            res = requests.get("http://"+get_url(prometheus['gcp']))
            print("gcp "+str(res.status_code))

        except requests.Timeout:
            print("gcp timeout")
            pass
        except requests.ConnectionError:
            print("gcp connectionerror")
            recovery("http://"+flask_api['gcp'])
            gcp = False
            pass
        finally:
            threading.Timer(20, gcp_connect_check).start()

@app.route('/')
def index():
    userid = session.get('userid', None)
    return render_template("index.html", userid=userid)

# 3개 클라우드의 그라파나 ip를 받아서 grafana-values.yaml 파일을 수정
@app.route('/grafana', methods=['GET', 'POST'])
def grafana():
    form = GrafanaForm()
    if form.validate_on_submit():
        with open('grafana-values.yaml', 'r', encoding='utf-8') as f:
	        ym = yaml.load(f, Loader=yaml.FullLoader)

        for elem in ym:
	        if elem == 'datasources':
		        newdict = ym[elem]
		        newdict = newdict['datasources.yaml']
		        newdict = newdict['datasources']
		        for elem in newdict:
			        if elem['name'] == 'aws':
				        elem['url'] = form.data.get('aws_ip')
			        elif elem['name'] == 'azure':
			    	    elem['url'] = form.data.get('azure_ip')
			        elif elem['name'] == 'gcp':
				        elem['url'] = form.data.get('gcp_ip')
        with open('grafana-values.yaml', 'w', encoding='utf-8') as f:
	        yaml.dump(ym, f)
        return redirect('/waiting')

    return render_template('grafana_setting.html', form=form)

@app.route('/waiting', methods=['GET', 'POST'])
def waiting():
    # ns 생성
    os.system('kubectl create namespace monitoring')
    # helm 설치 
    os.system('curl https://raw.githubusercontent.com/helm/helm/master/scripts/get > get_helm.sh')
    os.system('chmod 700 get_helm.sh')
    os.system('./get_helm.sh')
    # 사용자 클라우드에 helm으로 grafana 설치
    os.system('helm install grafana stable/grafana -f grafana-values.yaml --namespace monitoring')
    # 그라파나 ip를 받아와서 grafana_ip.txt에 저장
    os.system("kubectl get svc grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}' > grafana_ip.txt")
    
    # 설치가 완료되었는지 check
    while True:
        # grafana_ip.txt가 빈 파일이라면 삭제하고 다시 명령어 실행
        # 그라파나가 아직 설치되지않아 에러가 발생하면 grafana_ip.txt가 빈 파일로 저장됨
        if os.stat("grafana_ip.txt").st_size == 0:
                os.system('rm -rf grafana_ip.txt')
                os.system("kubectl get svc grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}' > grafana_ip.txt")
        else:
            break 
    return redirect('/register')

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
            fcuser.grafana_ip = open('grafana_ip.txt', 'r').read()
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
        # 저장경로는 web/yaml폴더
        # f.save(secure_filename('./yaml/'+f.filename))
        f.save(secure_filename('./yaml/'+'recovery.yaml'))
        return 'file uploaded successfully'

# 파일 보내기
# @app.route('/recovery')
def recovery(ip_address, **kwargs):
    # 쿼리스트링으로 ip주소 받음
    if 'target_namespace' not in kwargs.keys():
        target_namespace = 'default'
    else:
        target_namespace = kwargs['namespace']

    # 전송할 yaml파일 경로
    yaml_file_dir = './azure-vote-all-in-one-redis.yaml'

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
    aws_connect_check()
    # gcp_connect_check()

# 이 부분 추후 도커 패키징 시 kubernetes config에 따라 수정 필요
    app.run(host='0.0.0.0', port=80, debug=True)
