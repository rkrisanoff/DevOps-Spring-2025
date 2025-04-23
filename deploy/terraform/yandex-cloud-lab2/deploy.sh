wget -O /tmp/archive.tar.gz https://github.com/rkrisanoff/DevOps-Spring-2025/archive/refs/tags/v0.3.0.tar.gz
tar xf /tmp/archive.tar.gz -C /home/ubuntu/

cd /home/ubuntu/DevOps-Spring-2025-0.3.0
sudo docker compose up -d
