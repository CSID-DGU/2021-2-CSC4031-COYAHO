# Pod Deployment
```
$ kubectl apply -f 파일경로/nginx-deployment.yaml
```

# Helm Stable Charts을 이용해 클라우드 환경 구축

## Helm Repository에 Stable 추가
```
$ helm repo add stable https://charts.helm.sh/stable
```

## 새로운 Namespace 생성
```
$ kubectl create namespace monitoring
```

##  Prometheus, Grafana  설치 

### AWS, Azure, GCP
```
$ helm install prometheus stable/prometheus -f 파일경로/prometheus-values.yaml --namespace monitoring
```

### OCI
```
$ helm install prometheus stable/prometheus -f 파일경로/prometheus-values-oci.yaml --namespace monitoring
$ helm install grafana stable/grafana -f 파일경로/grafana-values.yaml --namespace monitoring 
```

# 주의사항
## 파일 경로 
Github에 업로드 된 파일을 사용하려면 경로를 다음과 같이 Raw 소스로 지정해야합니다.
![image](https://user-images.githubusercontent.com/65498159/136786804-23fec445-e1f2-4fc8-a1f0-ff7084e15f49.png)

이 소스를 ```$ wget 파일경로/파일이름.yaml```으로 직접 다운받아 로컬 경로에서 실행할 수도 있습니다.

## Grafana Login 
초기 설정은 ```User: admin``` ```Password: coyaho``` 입니다.

## Prometheus target, Grafana datasource
prometheus-values-oci.yaml의 targets와 grafana-values.yaml의 datasource는 각각 기본 값으로 설정되어 있으므로 target으로 하고자 하는 prometheus-server의 ip를 입력해서 사용하시면 됩니다.
