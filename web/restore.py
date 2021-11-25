
import requests
import threading
import os
import time
import yaml
import json

with open(os.path.join(os.path.dirname(__file__), 'cloud_info.json'), 'r') as f:
    cloud_info = json.load(f)


def get_url(prometheus_url):
    return prometheus_url


def get_namespace_list(csp):
    return 0


def recovery_send():
    problem_flag = False

    # 검사
    for idx, csp in enumerate(cloud_info.keys()):
        if csp == 'azure':
            azure_connect_check()
        elif csp == 'aws':
            aws_connect_check()
        elif csp == 'gcp':
            gcp_connect_check()

        csp_stat = cloud_info[csp]
        # 조건문으로 클라우드에서 응답없음 확인
        if csp_stat['status'] is False:
            print(f'{csp} 클라우드에서 응답이 없습니다.')
            try:
                # 문제가 발생한 클라우드의 인덱스+1을 csp_to_recover로 지정
                csp_to_recover = list(cloud_info.keys())[idx+1]
            except:
                # 마지막 순번의 클라우드에 문제가 발생할 경우 첫 번째 클라우드로 지정
                csp_to_recover = list(cloud_info.keys())[0]
            # 문제가 발생한 클라우드를 cloud_info에서 삭제
            cloud_info.pop(csp)
            print(f'{csp} 클라우드가 모니터링 대상에서 제외되었습니다.')
            print(list(cloud_info.keys()))
            # problem_flag True로 변경
            problem_flag = True
            break
        else:
            print(f'{csp} 클라우드가 정상 작동하고 있습니다.')
    print(cloud_info)
    # problem_flag가 True이면 복구기능 수행
    if problem_flag:
        # csp_to_recover에 복구명령 전달
        print(cloud_info)
        print(f'{csp_to_recover} 클라우드에서 복구명령을 수행합니다')
        # 복구 수행
        recovery(cloud_info[csp_to_recover]['api_ip'], target_namespace='test')
        print('복구가 완료되었습니다.')


def azure_connect_check():
    if cloud_info['azure']['status']:
        try:
            res = requests.get(
                "http://{}".format(get_url(cloud_info['azure']['prometheus_ip'])))
            print("azure response status code :"+str(res.status_code))
        except requests.Timeout:
            print("azure timeout")
            pass
        except requests.ConnectionError:
            print("azure connectionerror")
            # recovery(
            #    "http://{}".format(get_url(cloud_info['azure']['api_ip'])))
            cloud_info['azure']['status'] = False
            pass
        # finally:
        #    threading.Timer(20, azure_connect_check).start()


def aws_connect_check():
    if cloud_info['aws']['status']:
        try:
            res = requests.get(
                "http://{}".format(get_url(cloud_info['aws']['prometheus_ip'])))
            print("aws response status code :"+str(res.status_code))

        except requests.Timeout:
            print("aws timeout")
            pass
        except requests.ConnectionError:
            print("aws connectionerror")
            # recovery("http://{}".format(get_url(cloud_info['aws']['api_ip'])))
            cloud_info['aws']['status'] = False
            pass
        # finally:
        #    threading.Timer(20, aws_connect_check).start()


def gcp_connect_check():
    if cloud_info['azure']['status']:
        try:
            res = requests.get(
                "http://{}".format(get_url(cloud_info['gcp']['prometheus_ip'])))
            print("gcp response status code :"+str(res.status_code))

        except requests.Timeout:
            print("gcp timeout")
            pass
        except requests.ConnectionError:
            print("gcp connectionerror")
            # recovery("http://{}".format(get_url(cloud_info['gcp']['api_ip'])))
            cloud_info['gcp']['status'] = False
            pass
        # finally:
        #    threading.Timer(20, gcp_connect_check).start()


def recovery(ip_address, **kwargs):
    # 쿼리스트링으로 ip주소 받음
    if 'target_namespace' not in kwargs.keys():
        target_namespace = 'default'
    else:
        target_namespace = kwargs['target_namespace']

    # 전송할 yaml파일 경로
    yaml_file_dir = '.\\yaml\\recovery.yaml'

    sample_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.1.2222.33 Safari/537.36",
        "Accept-Encoding": "*",
        "Connection": "keep-alive"
    }

    def send_request(**kwargs):
        if 'target_URL' not in kwargs.keys() or 'kind' not in kwargs.keys() or 'yaml_data' not in kwargs.keys():
            raise Exception('필수 매개변수가 없습니다.')

        # requests.post("http://"+target_URL+'/'+recovery_type +
        #              f'/post?namespace={target_namespace}', json=yaml_data, headers=sample_headers)
        print("[[http://{}/{}/post?namespace={}]]".format(kwargs['target_URL'],
                                                          kwargs['kind'], kwargs['target_namespace']))

    with open(os.path.join(os.path.dirname(__file__), yaml_file_dir)) as f:
        dep = list(yaml.safe_load_all(f))
        for i in range(len(dep)):
            time.sleep(5)
            print(dep[i])
            recovery_type = dep[i]['kind'].lower()
            send_request(target_URL=ip_address,
                         kind=recovery_type, yaml_data=(dep[i]), target_namespace=target_namespace)
    print('okay')
    return 'file sent successfully'


if __name__ == "__main__":
    print('[탐지 및 복구기능을 시작합니다.]')
    recovery_send()
