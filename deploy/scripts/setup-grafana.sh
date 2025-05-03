sudo apt-get install -y adduser libfontconfig1 musl
wget -O /tmp/grafana.deb https://dl.grafana.com/oss/release/grafana_11.6.1_amd64.deb

sudo dpkg -i /tmp/grafana.deb

sudo cp /home/ubuntu/grafana_provisioning/dashboards/* /etc/grafana/provisioning/dashboards/
sudo cp /home/ubuntu/grafana_provisioning/datasources/* /etc/grafana/provisioning/datasources/

sudo systemctl daemon-reload
sudo systemctl start grafana-server
