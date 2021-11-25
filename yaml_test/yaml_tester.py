import requests
import yaml
from os import path

ip_address = 'http://34.72.9.91'
yaml_file_dir = "test2.yaml"


def send_request(target_URL=None, kind=None, yaml_data=None):
    requests.post(target_URL+'/'+kind+'/post', json=yaml_data)
    print(yaml_data)
    print()
    print(target_URL+'/'+kind+'/post')


with open(path.join(path.dirname(__file__), yaml_file_dir)) as f:
    dep = list(yaml.safe_load_all(f))
    for i in range(len(dep)):
        kind = dep[i]['kind'].lower()
        send_request(target_URL=ip_address,
                     kind=kind, yaml_data=(dep[i]))
