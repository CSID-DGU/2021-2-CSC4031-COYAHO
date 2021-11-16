from flask import Blueprint, request
from api import utils

restore_api = Blueprint('restore', __name__)


@restore_api.route('/do_restore', methods=['GET'])
def restore():
    utils.create_from_yaml.create_from_yaml()
