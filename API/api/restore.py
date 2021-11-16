from flask import Blueprint, request
from kubernetes import utils
from api import kube_config

restore_api = Blueprint('restore', __name__)


@restore_api.route('/post', methods=['POST'])
def post():
    yaml_data = request.get_json()
    utils.create_from_yaml(k8s_client=kube_config, yaml_objects=[yaml_data])
    return {'yaml': yaml_data}
