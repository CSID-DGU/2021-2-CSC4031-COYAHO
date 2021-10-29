---
page_type: sample
languages:
  - python
products:
  - azure
  - azure-redis-cache
description: "This sample creates a multi-container application in an Azure Kubernetes Service (AKS) cluster."
---

# Azure Voting App

This sample creates a multi-container application in an Azure Kubernetes Service (AKS) cluster. The application interface has been built using Python / Flask. The data component is using Redis.

To walk through a quick deployment of this application, see the AKS [quick start](https://docs.microsoft.com/en-us/azure/aks/kubernetes-walkthrough?WT.mc_id=none-github-nepeters).

To walk through a complete experience where this code is packaged into container images, uploaded to Azure Container Registry, and then run in and AKS cluster, see the [AKS tutorials](https://docs.microsoft.com/en-us/azure/aks/tutorial-kubernetes-prepare-app?WT.mc_id=none-github-nepeters).

<br>

## **🐳Docker Image 만들기** (로컬에서 진행)

1. 디렉토리 변경

   ```powershell
   cd azure-voting-app-redis
   ```

   <br>

2. docker-compose.yaml 파일을 사용하여 컨테이너 이미지 만들고, redis 이미지 다운로드하고 애플리케이션 시작

   ```powershell
   docker-compose up -d
   ```

- 본 서비스는 컨테이너 이미지가 2개라서 docker-compose를 사용한다 (docker-compose: 도커 이미지가 여러 개 있을 때 조금 더 빠르고 손쉽게 할 수 있는 명령 툴)
- docker-compose를 사용해서 컨테이너를 프로세스 업 시키면 이미지도 다운로드하고 지금 프로세스도 컨테이너에 대해서 올라가 있음

<br>

3.  만들어진 이미지를 확인한다(실질적으로 컨테이너가 어떻게 로컬에 저장되어있는지 확인)

    ```powershell
    docker images
    ```

- azure-vote-front 이미지에는 프런트 앤드 애플리케이션이 포함되어 있으며 nginx-flask 이미지를 기준으로 사용

- redis 이미지는 Redis 인스턴스를 시작하는 데 사용  
  <br>

4. 실행 중인 컨테이너 확인

   ```powershell
   docker ps
   ```

5. 실행중인 컨테이너 중지하고 제거하려면

   ```powershell
   docker-compose down
   ```

## **🔑컨테이너 레지스트리에 애플리케이션 업로드** (로컬에서 진행)

1. 컨테이너 레지스트리 만들기
2. 껍데기(레지스트리)가 만들어져서 만들어진 레지스트리를 가지고서 진행

> ### AWS

<br>

> ### Azure

1. 로컬에서 컨테이너 레지스트리에 접속

   - 컨테이너 레지스트리에 로그인

   ```powershell
   docker login <로그인 서버>
   ex) docker login coyahov2.azurecr.io
   ```

   - 이름과 패스워드는 왼쪽의 '엑세스 키'에 관리사용자 사용으로 하면 보임 (password는 복붙해도 화면에 안뜨니까 복붙하고 엔터해도 로그인 성공)

2. nginx를 레지스트리에 업로드하도록 이미지에 tag를 지정

   - 이미지 이름은 docker-compose.yaml에 작성한 이미지 이름을 넣어야 함

   ```powershell
   docker tag <이미지 이름> <이미지 저장소>/<tag 이름>
   ex) docker tag mcr.microsoft.com/azuredocs/azure-vote-front:v1 coyahov2.azurecr.io/azure-vote-front
   ```

3. nginx를 레지스트리에 푸시
   ```powershell
   docker push <이미지 저장소>/<tag 이름>
   ex) docker push coyahov2.azurecr.io/azure-vote-front
   ```
4. redis를 레지스트리에 업로드하도록 이미지에 tag를 지정

   ```powershell
   docker tag <이미지 이름> <이미지 저장소>/<tag 이름>
   ex) docker tag mcr.microsoft.com/oss/bitnami/redis:6.0.8 coyahov2.azurecr.io/redis
   ```

5. redis를 레지스트리에 푸시

   ```powershell
   docker push <이미지 저장소>/<tag 이름>
   ex) docker push coyahov2.azurecr.io/redis
   ```

   <br>

> ### GCP

<br>

## **🕸쿠버네티스 클러스터 만들고 배포하기**

> ### AWS

<br>

> ### Azure
>
> ACR과 연동해서 사용할 수 있도록

1. 인증>클러스터 인프라>시스템에서 할당한 관리 id 선택
2. 통합> ACR> 컨테이너 레지스트리 선택

하여 클러스터 구성

<br>
클러스터와 연결하고

```powershell
kubectl apply -f azure-vote-all-in-one-redis.yaml
```

로 pod와 svc 생성

> ### GCP

<br>

## **👀Autoscaling test**

로드가 왔을 때 로드의 정보를 확실히 보고 애플리케이션을 확장할 수 있음 ▶ 쿠버네티스의 HPA 기능을 이용해서 얼마나 빠르게 컨테이너가 확장되는지 확인

```powershell
kubectl autoscale deployment --max=10 azure-vote-front --min=3
```

로드가 없을 때는 최소 3개 떠있고 로드가 추가로 들어올 경우 컨테이너가 최대 10개까지 늘어남

로드를 주는 것은 azure의 로드 제너레이터를 이용하여 진행

```powershell
az container create -g <리소스 이름> -n loadtestnew --image azch/loadtest -e SERVICE_ENDPOINT=<external IP주소>  --restart-policy Never --no-wait
```

<br>

## Contributing

This project welcomes contributions and suggestions. Most contributions require you to agree to a
Contributor License Agreement (CLA) declaring that you have the right to, and actually do, grant us
the rights to use your contribution. For details, visit https://cla.microsoft.com.

When you submit a pull request, a CLA-bot will automatically determine whether you need to provide
a CLA and decorate the PR appropriately (e.g., label, comment). Simply follow the instructions
provided by the bot. You will only need to do this once across all repos using our CLA.

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/).
For more information see the [Code of Conduct FAQ](https://opensource.microsoft.com/codeofconduct/faq/) or
contact [opencode@microsoft.com](mailto:opencode@microsoft.com) with any additional questions or comments.
