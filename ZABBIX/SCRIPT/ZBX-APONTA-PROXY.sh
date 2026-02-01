#!/bin/bash

sed -i 's/^Server=127\.0\.0\.1$/Server=<ip_zabbix>/' /etc/zabbix/zabbix_agent2.conf
sleep 3s;
sed -i 's/^ServerActive=127\.0\.0\.1$/ServerActive=<ip_zabbix>/' /etc/zabbix/zabbix_agent2.conf


