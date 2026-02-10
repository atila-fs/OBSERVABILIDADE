#!/bin/bash
wget https://github.com/prometheus/prometheus/releases/download/v3.9.1/prometheus-3.9.1.linux-amd64.tar.gz
groupadd --system prometheus
useradd -s /sbin/nologin --system -g prometheus prometheus
mkdir /var/lib/prometheus
mkdir -p /etc/prometheus/rules
mkdir -p /etc/prometheus/rules.s
mkdir -p /etc/prometheus/files_sd
cd /opt/observability
tar xvf prometheus-3.9.1.linux-amd64.tar.gz
cd  prometheus-3.9.1.linux-amd64
mv prometheus promtool /usr/local/bin/
prometheus --version
mv prometheus.yml /etc/prometheus/prometheus.yml
tee /etc/systemd/system/prometheus.service<<EOF
[Unit]
Description=Prometheus
Documentation=https://prometheus.io/docs/introduction/overview/
Wants=network-online.target
After=network-online.target

[Service]
Type=simple
User=prometheus
Group=prometheus
ExecReload=/bin/kill -HUP $MAINPID
ExecStart=/usr/local/bin/prometheus \
          --config.file=/etc/prometheus/prometheus.yml \
            --storage.tsdb.path=/var/lib/prometheus \
              --web.console.templates=/etc/prometheus/consoles \
                --web.console.libraries=/etc/prometheus/console_libraries \
                  --web.listen-address=0.0.0.0:9090 \
                    --web.external-url=

SyslogIdentifier=prometheus
Restart=always

[Install]
WantedBy=multi-user.target
EOF
chown -R prometheus:prometheus /etc/prometheus
chown -R prometheus:prometheus /etc/prometheus/*
chmod -R 775 /etc/prometheus
chmod -R 775 /etc/prometheus/*
chown -R prometheus:prometheus /var/lib/prometheus
systemctl daemon-reload
systemctl start prometheus
systemctl enable prometheus
systemctl status prometheus
ss -tulpn | grep ":9090"