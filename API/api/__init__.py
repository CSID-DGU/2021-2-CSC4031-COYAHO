from flask import Flask
from kubernetes import client, config, utils

# 쿠버네티스 incluster 인증
config.load_incluster_config()
kube_config = client
kube_utils = utils
core_v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
