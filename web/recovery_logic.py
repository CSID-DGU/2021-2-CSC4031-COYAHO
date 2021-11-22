cloud_info = {'azure': {'ip': '0.0.0.0', 'status': True}, 'aws': {
    'ip': '0.0.0.1', 'status': True}, 'gcp': {'ip': '0.0.0.2', 'status': False}}


def recovery_send():
    problem_flag = False

    # 검사
    for idx, csp in enumerate(cloud_info.keys()):
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
            # problem_flag True로 변경
            problem_flag = True

            break
        else:
            print(f'{csp} 클라우드가 정상 작동하고 있습니다.')

    # problem_flag가 True이면 복구기능 수행
    if problem_flag:
        # csp_to_recover에 복구명령 전달
        print(cloud_info)
        print(f'{csp_to_recover} 클라우드에서 복구명령을 수행합니다')
        # 복구 수행
        print('복구가 완료되었습니다.')


recovery_send()
