wget -O /tmp/prometheus.tar.gz https://github.com/prometheus/prometheus/releases/download/v2.55.1/prometheus-2.55.1.linux-amd64.tar.gz

sudo tar xf /tmp/prometheus.tar.gz -C /usr/local/bin/
sudo chmod +x /usr/local/bin/prometheus-2.55.1.linux-amd64/prometheus

sudo mkdir -p /etc/prometheus/
sudo cp /home/ubuntu/prometheus/prometheus.yml /etc/prometheus/prometheus.yml
sudo cp /home/ubuntu/prometheus/prometheus.service /etc/systemd/system/prometheus.service

sudo useradd --no-create-home --shell /bin/false prometheus
sudo mkdir -p /var/lib/prometheus && sudo chown prometheus:prometheus /var/lib/prometheus

sudo systemctl daemon-reload
sudo systemctl start prometheus
