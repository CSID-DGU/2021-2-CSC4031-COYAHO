from flask import Blueprint, Flask, request
from kubernetes import client, config
from kubernetes.client.rest import ApiException
import time
from api import core_v1

namespace_api = Blueprint('namespace_api',__name__)

@namespace_api.route('/', methods=['POST'])
def namespaces():
	namespace = request.form['name']
	ret =  create_namespace(namespace)
	if ret != None:
		return "finish"
	else:
		return "fail"

@namespace_api.route('/<namespace>', methods=['GET','DELETE'])
def namespace(namespace):
	if request.method == 'GET':
		if read_namespace(namespace) != -1:
			return "get"
	else:
		if delete_namespace(namespace) != -1:
			return "delete"
	return "fail"

def create_namespace(namespace):
	body = {
		"metadata" : {
			"name" : namespace
		}
	}
	try:
		return core_v1.create_namespace(body=body)
	except ApiException as ex:
		return "error"

def read_namespace(namespace, timeout = 30):
	start_time = time.time()
	while True:
		try:
			ret = core_v1.read_namespace(namespace)
			return (ret)
		except Exception:
			time.sleep(1)
			if time.time() - start_time > timeout:
				raise TimeoutError
	return (-1)

def delete_namespace(namespace, timeout = 30):
	try:
		core_v1.delete_namespace(namespace)
	except ApiException as ex:
		# Already deleted
		if ex.status == 404:
			return (-1)
	start_time = time.time()
	while True:
		try:
			core_v1.read_namespace(namespace)
		except ApiException as ex:
			# Delete namespace finished
			if ex.status == 404:
				return (0)
		except Exception:
			time.sleep(1)
			if time.time() - start_time > timeout:
				raise TimeoutError
	return (-1)