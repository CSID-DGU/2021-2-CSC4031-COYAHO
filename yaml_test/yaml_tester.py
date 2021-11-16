from flask.globals import request
import requests
import yaml
import json
from os import path


def send_request(target_URL=None, kind=None, yaml_data=None):
    requests.post(target_URL+'/'+kind, json=yaml_data)


with open(path.join(path.dirname(__file__), "test.yaml")) as f:
    dep = list(yaml.safe_load_all(f))
    for i in range(len(dep)):
        kind = dep[i]['kind']
        send_request('http://35.202.218.39',
                     kind='restore/post', yaml_data=(dep[i]))
        # print(json.dumps(dep[i]))
        break
