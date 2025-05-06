# Деплой проекта на облаке Yandex.Cloud при помощи terraform
0. Указать путь к `.terraformrc`: `export TF_CLI_CONFIG_FILE=<PATH-TO-TERRAFORMRC>`
1. Создать, подключить аккаунт Яндекс.Облака. Создать пару ssh-ключей для доступа. Установить переменные среды для доступа `yc` из консоли:
    ```bash
    export YC_TOKEN=$(yc iam create-token)
    export YC_CLOUD_ID=$(yc config get cloud-id)
    export YC_FOLDER_ID=$(yc config get folder-id)
    ```
2. Настроить зеркало для провайдеров terraform.
3. Создать конфигурацию образа: добавить необходимых пользователей, их права и ключи в `cloud-init.txt` (пример - `cloud-init-example.txt`)
4. Запустить проект целиком:
    ```bash
    cd deploy/
    bash deploy.sh
    ```

Для остановки виртуальной машины используется команда `terraform destroy --auto-approve`.

## Запуск поэтапно
Выполняется из директории `deploy` и окружения с установленным и настроенным Ansible.

### Terraform
```bash
terraform init
terraform apply --auto-approve
```

### Ansible
```bash
export EXTERNAL_IP=$(terraform output -raw external_ip_address)
echo 'external ip: ' $EXTERNAL_IP

export ANSIBLE_HOST_KEY_CHECKING=False
export ANSIBLE_SSH_PRIVATE_KEY="/home/anastasia/.ssh/yandex-cloud"
export ANSIBLE_USER="ubuntu"

ansible-playbook --inventory "${EXTERNAL_IP}," \
                 --user "${ANSIBLE_USER}" \
                 --extra-vars "ansible_ssh_private_key_file=${ANSIBLE_SSH_PRIVATE_KEY}" \
                 playbooks/deploy-services.yml -v

ansible-playbook --inventory "${EXTERNAL_IP}," \
                 --user "${ANSIBLE_USER}" \
                 --extra-vars "ansible_ssh_private_key_file=${ANSIBLE_SSH_PRIVATE_KEY}" \
                 playbooks/deploy-metrics.yml -v
```


## Патчи для HPA
```bash
kubectl patch hpa backend-hpa --type=json -p='[{"op":"replace", "path": "/spec/metrics/0/resource/target/averageUtilization", "value":30}]'
```
