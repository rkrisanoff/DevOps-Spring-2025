# Frontend DevOps-Spring-2025

Фронтенд для проекта DevOps-Spring-2025 (заготовка).

## Технологии
* Python, Django
* Js + CSS

## Разработка

Запуск веб-сервиса внутри контейнера:
```bash
uv run python manage.py runserver 0.0.0.0:8005
```

dev-запуск отдельного контейнера:
```bash
docker run -it --rm --entrypoint /bin/bash -v .:/frontend -p 8002:8005 --name frontend-dev frontend
```
В этом случае в `frontend/` появится папка `.venv`, отвечающая за окружение внутри контейнера.

prod-запуск отдельного контейнера:
```bash 
docker run --rm -d -p 8002:8005 --name frontend-prod frontend
```

### TODO-list:
* настроить запросы к серверу с retry и т.д.
* добавить обновление БД по кнопке show (сейчас показывает только то, что есть в памяти)
* оставить пустую таблицу в main_screen по умолчанию, обновлять при показе