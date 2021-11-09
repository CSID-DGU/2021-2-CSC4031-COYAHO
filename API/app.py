from flask import Flask, request
from api import namespace, deployment
from api import core_v1

app = Flask(__name__)

# namespace 관련
app.register_blueprint(namespace.namespace_api, url_prefix='/namespace')
app.register_blueprint(deployment.deployment_api, url_prefix='/deployment')

# 기본 페이지
@app.route("/")
def welcome():
    return "welcome to service"

# pod 조회 예시
@app.route("/pods")
def get_deploy():
    podlist = []
    print("Listing pods and IPs")
    ret = core_v1.list_pod_for_all_namespaces(watch=False)
    for i in ret.items:
        podlist.append(
            [i.status.pod_ip, i.metadata.namespace, i.metadata.name])
    example = {'podlist': podlist}
    return example


# host='0.0.0.0',debug=True, port=80
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=80)
