# -*-coding utf-8-*-
from flask import Flask
from kubernetes import client, config

#쿠버네티스 incluster 인증
config.load_incluster_config()
core_v1 = client.CoreV1Api()