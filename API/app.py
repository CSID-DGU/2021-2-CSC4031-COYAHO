from flask import Flask, request
from api import namespace
from api import core_v1

app = Flask(__name__)
app.register_blueprint(namespace.namespace_api, url_prefix='/namespaces')

@app.route("/")
def welcome():
    return "welcome to service"

@app.route("/deployment")
def get_deploy():
    podlist=[]
    print("Listing pods and IPs")
    ret = core_v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        podlist.append([i.status.pod_ip, i.metadata.namespace, i.metadata.name])
    example={'podlist':podlist}
    return example

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True, port=80)