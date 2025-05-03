wget -O /tmp/archive.tar.gz https://github.com/rkrisanoff/DevOps-Spring-2025/archive/refs/tags/v0.2.4.tar.gz
tar xf /tmp/archive.tar.gz -C /home/ubuntu/

cd /home/ubuntu/DevOps-Spring-2025-0.2.4
sudo docker compose up -d
