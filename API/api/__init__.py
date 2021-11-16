from flask import Flask
from kubernetes import client, config

# 쿠버네티스 incluster 인증
config.load_incluster_config()
kube_config = client
core_v1 = client.CoreV1Api()
apps_v1 = client.AppsV1Api()
