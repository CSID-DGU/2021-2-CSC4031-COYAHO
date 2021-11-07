from flask import Blueprint, request
from api import apps_v1
from os import path
import yaml

deployment_api = Blueprint('deployment',__name__)

@deployment_api.route('/<deployment>', methods=['POST', 'GET', 'DELETE'])
def deployment(deployment):
    if request.method == "POST":
        target_namespace=request.args.get('namespace')
        if target_namespace:
            return create_deployment(namespace=target_namespace)
        else:
            return create_deployment()
    
    elif request.method == "GET":
        return get_deployment(deployment)

    elif request.method == "DELETE":
	    return delete_deployment(deployment)

#yaml 불러와 디플로이먼트 생성
def create_deployment(**kwargs):
    if 'namespace' not in kwargs.keys():
        target_namespace='default'
    else:
        target_namespace=kwargs['namespace']

    #시험용 코드이므로 작동확인 후 원하는 기능에 맞춰 수정예정
    with open(path.join(path.dirname(__file__), "test-deployment.yaml")) as f:
        dep = yaml.safe_load(f)
        resp = apps_v1.create_namespaced_deployment(
            body=dep, namespace=target_namespace)
    return {'message':"Deployment created. status='%s'" % resp.metadata.name}

def get_deployment():
    return {'message':'under construction'}

def delete_deployment():
    return {'message':'under construction'}