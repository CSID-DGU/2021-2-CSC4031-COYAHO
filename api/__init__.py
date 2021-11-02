from flask import Flask
import os
from kubernetes import client, config

kubeconfig = os.getenv('KUBECONFIG')
config.load_kube_config(kubeconfig)
v1 = client.CoreV1Api()