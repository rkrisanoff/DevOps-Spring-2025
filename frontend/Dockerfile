FROM ubuntu:noble-20250127

RUN apt-get update && apt-get install -y python3-dev python3-pip
WORKDIR /frontend

COPY . .
RUN pip install -r requirements.txt --break-system-packages

EXPOSE 8000

ENTRYPOINT  [ "python3", "manage.py", "runserver", "0.0.0.0:8005" ]