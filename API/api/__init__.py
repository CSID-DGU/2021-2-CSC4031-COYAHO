from flask import Flask
import os
from kubernetes import client, config

config.load_incluster_config()
core_v1 = client.CoreV1Api()