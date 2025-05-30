# Деплой проекта на виртуальной машине/удаленном сервере

## Деплой проекта на облаке Yandex.Cloud при помощи terraform
1. Создать, подключить аккаунт Яндекс.Облака. Создать пару ssh-ключей для доступа. Установить переменные среды для доступа `yc` из консоли:
    ```bash
    export YC_TOKEN=$(yc iam create-token)
    export YC_CLOUD_ID=$(yc config get cloud-id)
    export YC_FOLDER_ID=$(yc config get folder-id)
    ```
2. Настроить зеркало для провайдеров terraform.
3. Создать конфигурацию образа: добавить необходимых пользователей, их права и ключи в `cloud-init.txt` (пример - `cloud-init-example.txt`)
4. Запустить проект:
    ```bash
    cd deploy/terraform/yandex-cloud/

    terraform init
    terraform plan
    terraform apply
    ```

Для остановки виртуальной машины используется команда `terraform destroy`.


## Деплой проекта при помощи Ansible на виртуальной машине
### Настройка Ansible и ролей
После установки Ansible необходимо установить нужные роли.
```bash
 ansible-galaxy role install geerlingguy.docker
```

Также перед тем, как разворачивать проект, необходимо задать системные переменные: `APP_TAG_VERSION` - версия проекта, скачиваемая с гитхаба, и `DEST_FOLDER` - папка на гостевой машине, в которую будет произведена распаковка архива. Можно установить вручную, можно через файл `config.env`.

Установка нужных системных переменных через файл `config.env`:
```bash
set -a
source config.env
set +a
```

### Хосты
Для запуска системы нужно создать файл `hosts.yml`, копирующий содержимое `hosts_example.yml`, но с подставленными значениями хоста, порта, пользователя на сервере и его пароля. На виртуальных машинах, созданных при помощи vagrant, логин/пароль - `vagrant`/`vagrant`.

### Плейбуки и их задачи
Запуск:
```bash
ansible-playbook -i hosts.yml <PLAYBOOK-FILENAME> --key-file keys/vm_key
```
`vagrant` для ssh-подключения используется автоматически сгенерированная пара ключей. Для простоты использования Ansible используется дополнительнаяя, сгенерированная заранее, пара ключей. Путь к ним указывается в параметре `--key-file`.

1. `test-connection.yml`: проверка подключения к серверу и попытка чтения системной переменной тега.

2. `deploy-booker-from-scratch.yml`: первое подключение к удаленному хосту: обновление пакетов, установка докера, скачивание исходного кода и его деплой через docker-compose.

3. `stop-deploy.yml`: остановка запущенных ранее контейнеров

4. `run-deploy.yml`: запуск контейнеров после остановки(при ранее установленном docker и скачанном коде).



## Создание виртуальных машин и деплой при помощи Vagrant
Создание виртуальных машин происходит при помощи утилиты [Vagrant](https://www.vagrantup.com/). Для этого нужно сделать следующие шаги:
1. Создать базовый образ виртуальной машины:
    * cкачать образ `ubuntu/jammy64` из облака публичных образов по [ссылке](https://portal.cloud.hashicorp.com/vagrant/discover).
    * создать образ по команде `vagrant box add --name ubuntu_vm <PATH_TO_FILE>`
2. Сгенерировать пару публичного и приватного ключа по имени `vm_key`, положить в папку `deploy/vagrant/keys`. Их этой папки они будут добавлены в виртуальную машину, чтобы к ней был доступ со стороны Ansible.
3. Перейти в директорию, где расположен `Vagrantfile` (`devops/vagrant`). Поднять виртуальную машину по команде `vagrant up --provision`. В случае, если на мастер-ноде установле Ansible, то автоматически будет выполнен деплой проекта.

### Нюансы работы в случае Windows
В том случае, если управляющий компьютер работает на ОС Windows, существует следующая проблема: Ansible может работать только на WSL, а Vagrant WSL не поддерживает. В данном случае нужно скопировать приватный ключ в `.ssh` папку WSL, установить права: `chmod 600 <PATH_TO_PRIVATE_KEY>`. При этом если ранее было подлючение по ssh на тот же хост, то нужно удалить предыдущие ключи командой  `ssh-keygen -f '~/.ssh/known_hosts' -R '<HOST>'`. Затем нужно подключиться по ssh для добавления хоста: `ssh vagrant@<HOST> -i <PATH_TO_PRIVATE_KEY>`.

В файле `ansible.cfg` нужно добавить следующее поле в блок `default`:
```bash
[defaults]
private_key_file: <PATH_TO_PRIVATE_KEY>
```

Из файла `Vagrantfile` нужно убрать строки, связанные с деплоем Ansible.

После этих операций можно создавать виртуальную машину и выполнять деплой проекта через плейбуки.
