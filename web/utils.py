import os
import json


def save_info(cloud_info):
    with open(os.path.join(os.path.dirname(__file__), 'cloud_info.json'), 'w') as f:
        json.dump(cloud_info, f)


def load_info():
    with open(os.path.join(os.path.dirname(__file__), 'cloud_info.json'), 'r') as f:
        cloud_info = json.load(f)
    return cloud_info
