#!/bin/bash

# Caminho do arquivo YAML
YAML_FILE="/home/administrator/scripts/validacao/fortinet-fortiadc-mib.yaml"

# Host e a comunidade SNMP
SNMP_HOST="172.30.200.20"
SNMP_COMMUNITY="safeweb_snmp"

# Função para extrair OIDs do arquivo YAML
extract_oids() {
    grep -oP '(?<=:\s)[\w\.\-]+' "$YAML_FILE"
}

# Validar se o arquivo YAML existe
if [[ ! -f "$YAML_FILE" ]]; then
    echo "Arquivo YAML $YAML_FILE não encontrado!"
    exit 1
fi

# Loop para percorrer cada OID extraída e executar o snmpwalk
echo "Executando snmpwalk para cada OID no arquivo $YAML_FILE..."
for oid in $(extract_oids); do
    echo "Executando snmpwalk para OID: $oid"
    snmpwalk -v2c -c "$SNMP_COMMUNITY" "$SNMP_HOST" "$oid"
done

echo "Execução finalizada."