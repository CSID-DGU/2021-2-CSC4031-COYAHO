from flask import Blueprint, request
from api import core_v1
from os import path
import yaml

service_api = Blueprint('service', __name__)


@service_api.route('/<service>', methods=['POST'])
def service(service):
    if request.method == "POST":
        target_namespace = request.args.get('namespace')
        if target_namespace:
            return create_service(namespace=target_namespace)
        else:
            return create_service()


def create_service(**kwargs):
    if 'namespace' not in kwargs.keys():
        target_namespace = 'default'
    else:
        target_namespace = kwargs['namespace']

    # 시험용 코드이므로 작동확인 후 원하는 기능에 맞춰 수정예정
    with open(path.join(path.dirname(__file__), "test-service.yaml")) as f:
        # yaml파일 내에 ---로 분리된 부분이 존재하는 경우 load가 아니라 load_all 사용해야함
        service = yaml.safe_load(f)
        resp = core_v1.create_namespaced_service(
            body=service, namespace=target_namespace)
    return {'message': "Service created. status='%s'" % resp.metadata.name}
