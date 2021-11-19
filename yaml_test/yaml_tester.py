from flask.globals import request
import requests
import yaml
from os import path

ip_address = 'http://35.202.218.39'
yaml_file_dir = "test.yaml"


def send_request(target_URL=None, kind=None, yaml_data=None):
    requests.post(target_URL+'/'+kind+'/post', json=yaml_data)


with open(path.join(path.dirname(__file__), yaml_file_dir)) as f:
    dep = list(yaml.safe_load_all(f))
    for i in range(len(dep)):
        kind = dep[i]['kind'].lower()
        send_request(target_URL=ip_address,
                     kind=kind, yaml_data=(dep[i]))
