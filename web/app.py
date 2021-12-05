from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, render_template, request, redirect, flash, session
from models import db
import os
from models import Fcuser
from flask_wtf.csrf import CSRFProtect
from forms import RegisterForm, LoginForm, UploadForm, GrafanaForm
from restore import recovery_send
from utils import save_info, load_info
''''
cloud_info = {'azure': {'prometheus_ip': '20.196.226.18', 'api_ip': '20.196.225.177', 'status': True},
              'aws': {'prometheus_ip': 'a790d6655f63c401c86fb7f46231d257-1084231655.us-west-2.elb.amazonaws.com', 'api_ip': 'ae50df8052d55419ab5df1bd7c72e9ef-1421424937.us-west-2.elb.amazonaws.com', 'status': True},
              'gcp': {'prometheus_ip': '34.121.224.0', 'api_ip': '34.134.51.2', 'status': True}}
'''
cloud_info = {'cloud1': {'prometheus_ip': '20.196.226.18', 'api_ip': '20.196.225.177', 'status': True},
              'cloud2': {'prometheus_ip': '35.224.146.53', 'api_ip': '35.193.214.43', 'status': True}}
save_info(cloud_info)

# APScheduler의 max_instance 에러로 복구가 실행되지 않는 경우가 있어 파라미터 2로 설정
scheduler = BackgroundScheduler(
    daemon=True, timezone='Asia/Seoul', job_defaults={'max_instances': 2})
scheduler.start()
scheduler.add_job(recovery_send, 'interval', seconds=30)

app = Flask(__name__)

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
        # 저장경로는 web/yaml/recovery.yaml
        savepath = '.\\yaml\\recovery.yaml'
        f.save(savepath)
        return 'file uploaded successfully'
    return redirect('/index')

###################### 복구 외 기능 ######################


@app.route('/')
def index():
    userid = session.get('userid', None)
    return render_template("index.html", userid=userid)

# 3개의 클라우드 ip와 api 서버 ip를 받아옴
@app.route('/grafana', methods=['GET', 'POST'])
def grafana():
    form = GrafanaForm()
    if form.validate_on_submit():

        cloud_info['aws']['prometheus_ip'] = form.data.get('aws_ip')
        cloud_info['azure']['prometheus_ip'] = form.data.get('azure_ip')
        cloud_info['gcp']['prometheus_ip'] = form.data.get('gcp_ip')
        cloud_info['aws']['api_ip'] = form.data.get('aws_api')
        cloud_info['azure']['api_ip'] = form.data.get('azure_api')
        cloud_info['gcp']['api_ip'] = form.data.get('gcp_api')
        save_info(cloud_info)

        return redirect('/register')

    '''
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
    '''
    return render_template('grafana_setting.html', form=form)


'''
@app.route('/waiting', methods=['GET', 'POST'])
def waiting():
    # ns 생성
    os.system('kubectl create namespace monitoring')
    # helm 설치 
    os.system('curl https://raw.githubusercontent.com/helm/helm/master/scripts/get > get_helm.sh')
    os.system('chmod 700 get_helm.sh')
    os.system('./get_helm.sh')
    # 사용자 클라우드에 helm으로 grafana 설치
    os.system(
        'helm install grafana stable/grafana -f grafana-values.yaml --namespace monitoring')
    # 그라파나 ip를 받아와서 grafana_ip.txt에 저장
    os.system(
        "kubectl get svc grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}' > grafana_ip.txt")

    # 설치가 완료되었는지 check
    while True:
        # grafana_ip.txt가 빈 파일이라면 삭제하고 다시 명령어 실행
        # 그라파나가 아직 설치되지않아 에러가 발생하면 grafana_ip.txt가 빈 파일로 저장됨
        if os.stat("grafana_ip.txt").st_size == 0:
            os.system('rm -rf grafana_ip.txt')
            os.system(
                "kubectl get svc grafana -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].ip}' > grafana_ip.txt")
        else:
            break
    return redirect('/register')
'''
# 회원 가입 기능
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
            db.session.add(fcuser)
            db.session.commit()

            # 회원가입 이후 recovery check start (딕셔너리가 공백이 아닐 경우)
            recovery_send()

            return render_template('index.html')

    return render_template('register.html', form=form)

# 로그인 기능
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

# 로그아웃 기능
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('userid', None)
    return redirect('/')

# 각 페이지 별 path 설정
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

# apscheduler 사용 시 두 번씩 중복작동하는 문제가 있어 reloader를 꺼놓도록 설정했습니다.
# 도커 패키징
    # app.run(host='0.0.0.0', port=80, debug=True, use_reloader=False)

# localhost 테스트
    app.run(host='127.0.0.1', port=5000, debug=True, use_reloader=False)
