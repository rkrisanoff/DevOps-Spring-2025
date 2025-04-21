```shell
yc iam service-account create --name terradevops
```

```
yc resource-manager folder add-access-binding <имя-каталога> \
  --role editor,vpc.user \
  --subject serviceAccount:<ID-сервисного-аккаунта>
```




```shell
export YC_TOKEN=$(yc iam create-token)
export YC_CLOUD_ID=$(yc config get cloud-id)
export YC_FOLDER_ID=$(yc config get folder-id)
```

```shell
 YC_TOKEN=$(yc iam create-token) terraform apply
```

```shell
 YC_TOKEN=$(yc iam create-token) terraform destroy
```


```shell
minikube service ingress-nginx-controller -n ingress-nginx
```
