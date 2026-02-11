#!/bin/bash
mkdir -p /opt/observability
cd /opt/observability
wget https://github.com/prometheus/node_exporter/releases/download/v1.10.2/node_exporter-1.10.2.linux-amd64.tar.gz
tar xvf node_exporter-1.10.2.linux-amd64.tar.gz
cd  node_exporter-1.10.2.linux-amd64
./node_exporter &   