from flask import Blueprint, request
from api import apps_v1
from os import path
import yaml

deployment_api = Blueprint('deployment', __name__)


@deployment_api.route('/<deployment>', methods=['POST', 'GET', 'DELETE'])
def deployment(deployment):
    if request.method == "POST":
        return create_deployment2()

    elif request.method == "GET":
        return get_deployment()

    elif request.method == "DELETE":
        return delete_deployment()

# yaml 불러와 디플로이먼트 생성


def create_deployment2(**kwargs):
    yaml_data = request.get_json()
    resp = apps_v1.create_namespaced_deployment(
        body=yaml_data, namespace="default")
    return {'message': "Deployment created. status='%s'" % resp.metadata.name}


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


def get_deployment():
    return {'message': 'under construction'}


def delete_deployment():
    return {'message': 'under construction'}