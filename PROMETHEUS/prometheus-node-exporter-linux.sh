#!/bin/bash
mkdir -p /opt/observability
cd /opt/observability
groupadd --system prometheus
useradd -s /sbin/nologin --system -g prometheus prometheus
wget https://github.com/prometheus/node_exporter/releases/download/v1.10.2/node_exporter-1.10.2.linux-amd64.tar.gz
tar xvf node_exporter-1.10.2.linux-amd64.tar.gz
cd  node_exporter-1.10.2.linux-amd64
mkdir -p /var/lib/node
cp node_exporter /var/lib/node
tee /etc/systemd/system/exporter.service<<EOF
[Unit]
Description=Prometheus Node Exporter
Documentation=https://prometheus.io/docs/introduction/overview/
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=prometheus
Group=prometheus
ExecReload=/bin/kill -HUP $MAINPID
ExecStart=/var/lib/node/node_exporter

SyslogIdentifier=prometheus_node_exporter
Restart=always

[Install]
WantedBy=multi-user.target
EOF
chown -R prometheus:prometheus /var/lib/node
chown -R prometheus:prometheus /var/lib/node/*
chmod -R 775 /var/lib/node
chmod -R 775 /var/lib/node/*
systemctl daemon-reload
systemctl enable exporter
systemctl start exporter
systemctl status exporter
ss -tulpn | grep ":9100"