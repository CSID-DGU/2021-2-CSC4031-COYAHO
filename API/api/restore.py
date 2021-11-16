from flask import Blueprint, request
from api import kube_config, kube_utils
from kubernetes import config, client, utils

restore_api = Blueprint('restore', __name__)


@restore_api.route('/post', methods=['POST'])
def post():
    yaml_data = request.get_json()
    kube_utils.create_from_yaml(k8s_client=kube_config, yaml_objects=[yaml_data])
    return {'yaml': yaml_data}

@restore_api.route('/post2', methods=['POST'])
def post2():
    config.load_incluster_config()
    yaml_data = request.get_json()
    utils.create_from_yaml(k8s_client=client, yaml_objects=[yaml_data])
    return {'yaml': yaml_data}

