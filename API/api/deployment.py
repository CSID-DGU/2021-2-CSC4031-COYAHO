from flask import Blueprint, request
from api import apps_v1

deployment_api = Blueprint('deployment', __name__)

# 아래 경로는 현재 미사용
@deployment_api.route('/<deployment>', methods=['GET', 'DELETE'])
def deployment(deployment):
    if request.method == "GET":
        return get_deployment()

    elif request.method == "DELETE":
        return delete_deployment()

# yaml 불러와 디플로이먼트 생성


@deployment_api.route('/post', methods=['POST'])
def create_deployment():
    # namespace가 query string으로 전달되지 않았을 경우 default namespace에 deploy 생성
    # json으로 dictionary 형태로 변환된 yaml 파일 전달받음
    namespace = request.args.get('namespace')
    yaml_data = request.get_json()

    if not namespace:
        namespace = "default"
    # deployment 생성
    resp = apps_v1.create_namespaced_deployment(
        body=yaml_data, namespace=namespace)
    return {'message': "Deployment created. status='%s'" % resp.metadata.name}


'''
def create_deployment(**kwargs):
    if 'namespace' not in kwargs.keys():
        target_namespace = 'default'
    else:
        target_namespace = kwargs['namespace']

    # 시험용 코드이므로 작동확인 후 원하는 기능에 맞춰 수정예정
    with open(path.join(path.dirname(__file__), "test-deployment.yaml")) as f:
        # yaml파일 내에 ---로 분리된 부분이 존재하는 경우 load가 아니라 load_all 사용해야함
        dep = yaml.safe_load(f)
        resp = apps_v1.create_namespaced_deployment(
            body=dep, namespace=target_namespace)
    return {'message': "Deployment created. status='%s'" % resp.metadata.name}

'''


def get_deployment():
    return {'message': 'under construction'}


def delete_deployment():
    return {'message': 'under construction'}
