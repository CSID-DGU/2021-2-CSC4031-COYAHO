from flask import Blueprint, Flask, request
from kubernetes.client.rest import ApiException
from api import core_v1
#import time

namespace_api = Blueprint('namespace', __name__)


@namespace_api.route('/<namespace>', methods=['POST', 'GET', 'DELETE'])
def namespace(namespace):
    if request.method == "POST":
        return create_namespace(namespace)

    elif request.method == "GET":
        return get_namespace()

    elif request.method == "DELETE":
        return delete_namespace(namespace)

# 네임스페이스 생성


def create_namespace(namespace):
    body = {
        "metadata": {
            "name": namespace
        }
    }
    try:
        core_v1.create_namespace(body=body)
    except ApiException as e:
        return message_handler(message="fail to CREATE namespace", exception=e)
    return message_handler(message="namespace created")

# 클러스터 내 모든 네임스페이스 조회


def get_namespace():
    list_namespace = core_v1.list_namespace()
    return {'result': list_namespace}

# 네임스페이스 삭제


def delete_namespace(namespace):
    try:
        core_v1.delete_namespace(namespace)
    except ApiException as e:
        return message_handler(message="fail to DELETE namespace", exception=e)

# return할 메시지를 딕셔너리 형태로 처리


def message_handler(**kwargs):
    if 'exception' not in kwargs.keys():
        return {'message': kwargs['message']}
    else:
        return {'message': kwargs['message'], 'error': kwargs['exception']}


'''
기존 코드 임시 주석처리 추후 삭제예정
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
'''
