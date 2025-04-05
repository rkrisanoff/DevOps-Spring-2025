# Бэкенд DevOps-Spring-2025

Бэкенд


## Миграции

Создание новой миграции
```shell
alembic --config=./etc/alembic.ini revision --autogenerate -m "Init"
```

Применение миграций
```shell
alembic --config=./etc/alembic.ini upgrade head
```
