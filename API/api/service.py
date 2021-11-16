from flask import Blueprint, Flask, request
from kubernetes.client.rest import ApiException
from api import core_v1

service_api = Blueprint('service', __name__)


@service_api.route('/post', methods=['POST'])
def create_service():
    # json으로 dictionary 형태로 변환된 yaml 파일 전달받음
    yaml_data = request.get_json()
    # svc 생성
    resp = core_v1.create_namespaced_service(
        namespace="default", body=yaml_data)
    return {'message': "Deployment created. status='%s'" % resp.metadata.name}
