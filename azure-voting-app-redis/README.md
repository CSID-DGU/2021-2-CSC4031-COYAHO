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

## **๐ณDocker Image ๋ง๋ค๊ธฐ** (๋ก์ปฌ์์ ์งํ)

1. ๋๋ ํ ๋ฆฌ ๋ณ๊ฒฝ

   ```powershell
   cd azure-voting-app-redis
   ```

   <br>

2. docker-compose.yaml ํ์ผ์ ์ฌ์ฉํ์ฌ ์ปจํ์ด๋ ์ด๋ฏธ์ง ๋ง๋ค๊ณ , redis ์ด๋ฏธ์ง ๋ค์ด๋ก๋ํ๊ณ  ์ ํ๋ฆฌ์ผ์ด์ ์์

   ```powershell
   docker-compose up -d
   ```

- ๋ณธ ์๋น์ค๋ ์ปจํ์ด๋ ์ด๋ฏธ์ง๊ฐ 2๊ฐ๋ผ์ docker-compose๋ฅผ ์ฌ์ฉํ๋ค (docker-compose: ๋์ปค ์ด๋ฏธ์ง๊ฐ ์ฌ๋ฌ ๊ฐ ์์ ๋ ์กฐ๊ธ ๋ ๋น ๋ฅด๊ณ  ์์ฝ๊ฒ ํ  ์ ์๋ ๋ช๋ น ํด)
- docker-compose๋ฅผ ์ฌ์ฉํด์ ์ปจํ์ด๋๋ฅผ ํ๋ก์ธ์ค ์ ์ํค๋ฉด ์ด๋ฏธ์ง๋ ๋ค์ด๋ก๋ํ๊ณ  ์ง๊ธ ํ๋ก์ธ์ค๋ ์ปจํ์ด๋์ ๋ํด์ ์ฌ๋ผ๊ฐ ์์

<br>

3.  ๋ง๋ค์ด์ง ์ด๋ฏธ์ง๋ฅผ ํ์ธํ๋ค(์ค์ง์ ์ผ๋ก ์ปจํ์ด๋๊ฐ ์ด๋ป๊ฒ ๋ก์ปฌ์ ์ ์ฅ๋์ด์๋์ง ํ์ธ)

    ```powershell
    docker images
    ```

- azure-vote-front ์ด๋ฏธ์ง์๋ ํ๋ฐํธ ์ค๋ ์ ํ๋ฆฌ์ผ์ด์์ด ํฌํจ๋์ด ์์ผ๋ฉฐ nginx-flask ์ด๋ฏธ์ง๋ฅผ ๊ธฐ์ค์ผ๋ก ์ฌ์ฉ

- redis ์ด๋ฏธ์ง๋ Redis ์ธ์คํด์ค๋ฅผ ์์ํ๋ ๋ฐ ์ฌ์ฉ  
  <br>

4. ์คํ ์ค์ธ ์ปจํ์ด๋ ํ์ธ

   ```powershell
   docker ps
   ```

5. ์คํ์ค์ธ ์ปจํ์ด๋ ์ค์งํ๊ณ  ์ ๊ฑฐํ๋ ค๋ฉด

   ```powershell
   docker-compose down
   ```

## **๐์ปจํ์ด๋ ๋ ์ง์คํธ๋ฆฌ์ ์ ํ๋ฆฌ์ผ์ด์ ์๋ก๋** (๋ก์ปฌ์์ ์งํ)

1. ์ปจํ์ด๋ ๋ ์ง์คํธ๋ฆฌ ๋ง๋ค๊ธฐ
2. ๊ป๋ฐ๊ธฐ(๋ ์ง์คํธ๋ฆฌ)๊ฐ ๋ง๋ค์ด์ ธ์ ๋ง๋ค์ด์ง ๋ ์ง์คํธ๋ฆฌ๋ฅผ ๊ฐ์ง๊ณ ์ ์งํ

> ### AWS

<br>

> ### Azure

1. ๋ก์ปฌ์์ ์ปจํ์ด๋ ๋ ์ง์คํธ๋ฆฌ์ ์ ์

   - ์ปจํ์ด๋ ๋ ์ง์คํธ๋ฆฌ์ ๋ก๊ทธ์ธ

   ```powershell
   docker login <๋ก๊ทธ์ธ ์๋ฒ>
   ex) docker login coyahov2.azurecr.io
   ```

   - ์ด๋ฆ๊ณผ ํจ์ค์๋๋ ์ผ์ชฝ์ '์์ธ์ค ํค'์ ๊ด๋ฆฌ์ฌ์ฉ์ ์ฌ์ฉ์ผ๋ก ํ๋ฉด ๋ณด์ (password๋ ๋ณต๋ถํด๋ ํ๋ฉด์ ์๋จ๋๊น ๋ณต๋ถํ๊ณ  ์ํฐํด๋ ๋ก๊ทธ์ธ ์ฑ๊ณต)

2. nginx๋ฅผ ๋ ์ง์คํธ๋ฆฌ์ ์๋ก๋ํ๋๋ก ์ด๋ฏธ์ง์ tag๋ฅผ ์ง์ 

   - ์ด๋ฏธ์ง ์ด๋ฆ์ docker-compose.yaml์ ์์ฑํ ์ด๋ฏธ์ง ์ด๋ฆ์ ๋ฃ์ด์ผ ํจ

   ```powershell
   docker tag <์ด๋ฏธ์ง ์ด๋ฆ> <์ด๋ฏธ์ง ์ ์ฅ์>/<tag ์ด๋ฆ>
   ex) docker tag mcr.microsoft.com/azuredocs/azure-vote-front:v1 coyahov2.azurecr.io/azure-vote-front
   ```

3. nginx๋ฅผ ๋ ์ง์คํธ๋ฆฌ์ ํธ์
   ```powershell
   docker push <์ด๋ฏธ์ง ์ ์ฅ์>/<tag ์ด๋ฆ>
   ex) docker push coyahov2.azurecr.io/azure-vote-front
   ```
4. redis๋ฅผ ๋ ์ง์คํธ๋ฆฌ์ ์๋ก๋ํ๋๋ก ์ด๋ฏธ์ง์ tag๋ฅผ ์ง์ 

   ```powershell
   docker tag <์ด๋ฏธ์ง ์ด๋ฆ> <์ด๋ฏธ์ง ์ ์ฅ์>/<tag ์ด๋ฆ>
   ex) docker tag mcr.microsoft.com/oss/bitnami/redis:6.0.8 coyahov2.azurecr.io/redis
   ```

5. redis๋ฅผ ๋ ์ง์คํธ๋ฆฌ์ ํธ์

   ```powershell
   docker push <์ด๋ฏธ์ง ์ ์ฅ์>/<tag ์ด๋ฆ>
   ex) docker push coyahov2.azurecr.io/redis
   ```

   <br>

> ### GCP

<br>

## **๐ธ์ฟ ๋ฒ๋คํฐ์ค ํด๋ฌ์คํฐ ๋ง๋ค๊ณ  ๋ฐฐํฌํ๊ธฐ**

> ### AWS
## Prerequisite
1. eks ํด๋ฌ์คํฐ 
2. IAM ์์ฑ(Administrator, AmazonEC2ContainerRegistryFullAccess, AmazonElasticContainerRegistryPublicFullAccess ๋ฃ์ด์ฃผ์) 

## ์ด๋ฏธ์ง ๋ง๋ค๊ธฐ
์ด๋ฏธ์ง ๋ง๋๋ ๊ณผ์ ์ ๋ก์ปฌ์์ ์งํํ์ต๋๋ค. (ํด๋๋ฅผ ํ๋ ๋ง๋ค์ด์ VS code์ฌ์ฉ)
   ```powershell
git clone https://github.com/Azure-Samples/azure-voting-app-redis.git
cd azure-voting-app-redis
docker-compose up -d
docker images
   ```
   
## ECR, ๋์ปค์ ๋ก๊ทธ์ธ ํ Tag, push
```powershell
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws/p8g9w4h0
   ```
   
Tagging
 ```powershell
docker tag mcr.microsoft.com/azuredocs/azure-vote-front:v1 public.ecr.aws/p8g9w4h0/votingapp:aws-vote-front   
  ```
   ```powershell
docker tag mcr.microsoft.com/azuredocs/azure-vote-front:v1 public.ecr.aws/p8g9w4h0/votingapp:redis
  ```
Push
   ```powershell
docker push public.ecr.aws/p8g9w4h0/votingapp:aws-vote-front 
  ```
   ```powershell
docker push public.ecr.aws/p8g9w4h0/votingapp:redis
  ```
  
## yamlํ์ผ ์์ ํ๊ณ  ๋ฐฐํฌํ๊ธฐ

1. azure-vote-all-in-one-redis.yaml ํ์ผ ์์ 
image: ecr -> repo -> image ๋๋ฅด๋ฉด ๋์ค๋ ๊ฒฝ๋ก๋ฅผ ๋ฃ์ด์ค

2. ์์ ํ ํ์ผ์ forkํ ๊นํ๋ธ repo์ ์๋ก๋ ํ Raw ๋ฒํผ ๋๋ฅด๊ธฐ
3. kubectl apply ๋ช๋ น์ด๋ก ๋ฐฐํฌ

<br>

> ### Azure
>
> ACR๊ณผ ์ฐ๋ํด์ ์ฌ์ฉํ  ์ ์๋๋ก

1. ์ธ์ฆ>ํด๋ฌ์คํฐ ์ธํ๋ผ>์์คํ์์ ํ ๋นํ ๊ด๋ฆฌ id ์ ํ
2. ํตํฉ> ACR> ์ปจํ์ด๋ ๋ ์ง์คํธ๋ฆฌ ์ ํ

ํ์ฌ ํด๋ฌ์คํฐ ๊ตฌ์ฑ

<br>
ํด๋ฌ์คํฐ์ ์ฐ๊ฒฐํ๊ณ 

```powershell
kubectl apply -f azure-vote-all-in-one-redis.yaml
```

๋ก pod์ svc ์์ฑ

> ### GCP

<br>

## **๐Autoscaling test**

๋ก๋๊ฐ ์์ ๋ ๋ก๋์ ์ ๋ณด๋ฅผ ํ์คํ ๋ณด๊ณ  ์ ํ๋ฆฌ์ผ์ด์์ ํ์ฅํ  ์ ์์ โถ ์ฟ ๋ฒ๋คํฐ์ค์ HPA ๊ธฐ๋ฅ์ ์ด์ฉํด์ ์ผ๋ง๋ ๋น ๋ฅด๊ฒ ์ปจํ์ด๋๊ฐ ํ์ฅ๋๋์ง ํ์ธ

```powershell
kubectl autoscale deployment --max=10 azure-vote-front --min=3
```

๋ก๋๊ฐ ์์ ๋๋ ์ต์ 3๊ฐ ๋ ์๊ณ  ๋ก๋๊ฐ ์ถ๊ฐ๋ก ๋ค์ด์ฌ ๊ฒฝ์ฐ ์ปจํ์ด๋๊ฐ ์ต๋ 10๊ฐ๊น์ง ๋์ด๋จ

๋ก๋๋ฅผ ์ฃผ๋ ๊ฒ์ azure์ ๋ก๋ ์ ๋๋ ์ดํฐ๋ฅผ ์ด์ฉํ์ฌ ์งํ

```powershell
az container create -g <๋ฆฌ์์ค ์ด๋ฆ> -n loadtestnew --image azch/loadtest -e SERVICE_ENDPOINT=<external IP์ฃผ์>  --restart-policy Never --no-wait
ex) az container create -g coyaho -n loadtestnew --image azch/loadtest -e SERVICE_ENDPOINT=http://20.41.112.xx  --restart-policy Never --no-wait
```

- endpoint๋ ๋ถํ๋ฅผ ์ค ๋ถ๋ถ์ด๋ฏ๋ก azure-vote-front์ ์ฐ๊ฒฐ๋์ด ์๋ url ์ฃผ์๋ฅผ ์ค.
- ์๋ก ์ด๋ฏธ์ง๋ฅผ ๋ง๋๋ ๊ฒ์ด๊ธฐ ๋๋ฌธ์ loadtestnew๋ก ์ค์ 
- ์ปจํ์ด๋ ์ด๋ฏธ์ง๋ฅผ ๋ง๋ค์ด์ ์ด ์ด๋ฏธ์ง๋ ๋ก๋๋ฅผ ์ฃผ๋ ์ญํ ์ ํจ

๋ก๋๊ฐ ์ ๋๋ก ๋ค์ด๊ฐ๋์ง ํ์ธํ๊ธฐ

```powershell
az container logs -g <๋ฆฌ์์ค ์ด๋ฆ> -n loadtestnew
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
