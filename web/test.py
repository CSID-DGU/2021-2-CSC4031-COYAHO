import json
import os

with open(os.path.join(os.path.dirname(__file__), 'cloud_info.json'), 'r') as st_json:
    print(json.load(st_json)['aws'])
