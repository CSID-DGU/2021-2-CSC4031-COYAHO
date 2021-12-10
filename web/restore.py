
import requests
import os
import time
import yaml
from utils import save_info, load_info


def get_url(url):
    return url


def get_namespace_list(csp):
    return 0


def recovery_send():
    cloud_info = load_info()
    # 검사
    for idx, csp in enumerate(cloud_info.keys()):
        if len(list(cloud_info.keys())) == 1:
            if connect_check(csp) == False:
                print('no access')
            else:
                print('가용 클러스터가 1개 {} 입니다.'.format(list(cloud_info.keys())))
                break
        # if csp in ['azure', 'aws', 'gcp']:
        if not connect_check(csp):
            print(f'{csp} 클라우드에서 응답이 없습니다.')
            try:
                # 문제가 발생한 클라우드의 인덱스+1을 csp_to_recover로 지정
                csp_to_recover = list(cloud_info.keys())[idx+1]
            except:
                # 마지막 순번의 클라우드에 문제가 발생할 경우 첫 번째 클라우드로 지정
                csp_to_recover = list(cloud_info.keys())[0]
            # 문제가 발생한 클라우드를 cloud_info에서 삭제
            cloud_info.pop(csp)
            save_info(cloud_info)
            print(
                f'{csp} 클라우드가 모니터링 대상에서 제외되었습니다. {list(cloud_info.keys())}를 계속 모니터링 합니다.')
            # csp_to_recover에 복구명령 전달
            print(f'{csp_to_recover} 클라우드에서 복구명령을 수행합니다')
            # 복구 수행
            recovery(cloud_info[csp_to_recover]
                     ['api_ip'])
            break
        else:
            print(f'{csp} 클라우드가 정상 작동하고 있습니다.')


def connect_check(csp):
    cloud_info = load_info()
    if cloud_info[csp]['status']:
        try:
            res = requests.get(
                "http://{}".format(get_url(cloud_info[csp]['prometheus_ip'])))
            print("{} response status code : {}".format(
                csp, str(res.status_code)))
            return True
        except requests.Timeout:
            print("{} timeout".format(csp))
            return False
        except requests.ConnectionError:
            print("{} connectionerror".format(csp))
            cloud_info[csp]['status'] = False
            save_info(cloud_info)
            return False


def recovery(ip_address, **kwargs):
    '''
    if 'target_namespace' not in kwargs.keys():
        target_namespace = 'default'
    else:
        target_namespace = kwargs['target_namespace']
    '''
    target_namespace = 'restore'
    # 전송할 yaml파일 경로
    yaml_file_dir = '.\\yaml\\recovery.yaml'

    sample_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.1.2222.33 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }

    def send_request(**kwargs):
        if 'target_URL' not in kwargs.keys() or 'kind' not in kwargs.keys():
            raise Exception('필수 매개변수가 없습니다.')
        request_to_send = "http://{}/{}/post?namespace={}".format(
            kwargs['target_URL'], kwargs['kind'], kwargs['target_namespace'])
        try:
            requests.post(request_to_send, json=kwargs['yaml_data'])
        except:
            print('request 전송에 문제가 발생했습니다.')
        print(request_to_send)

    namespace_yaml = {
        "metadata": {
            "name": target_namespace
        }
    }
    send_request(target_URL=ip_address, kind='namespace',
                 target_namespace=target_namespace, yaml_data=namespace_yaml)

    with open(os.path.join(os.path.dirname(__file__), yaml_file_dir)) as f:
        try:
            dep = list(yaml.safe_load_all(f))
        except:
            print('복구를 위한 yaml파일을 불러오는데 실패했습니다.')
        else:
            for i in range(len(dep)):
                time.sleep(1)
                print('{}:{}에 대한 복구요청을 전송합니다.'.format(
                    dep[i]['kind'].lower(), dep[i]['metadata']['name']))
                send_request(target_URL=ip_address,
                             kind=dep[i]['kind'].lower(), yaml_data=(dep[i]), target_namespace=target_namespace)
            return 'file sent successfully'


if __name__ == "__main__":
    print('[탐지 및 복구기능을 시작합니다.]')
    recovery_send()
