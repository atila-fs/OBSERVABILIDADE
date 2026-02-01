#!/bin/bash

# Define o arquivo que contém as linhas
FILE="/var/log/relatorio-iti/data"

# Define o limite de 7 dias atrás
LIMIT_DATE=$(date -d '7 days ago' +%s)

# Loop através de cada linha do arquivo
while IFS= read -r line; do
    # Remove caracteres indesejados
    line=$(echo "$line" | tr -d '\r' | sed 's/^[ \t]*//;s/[ \t]*$//')

    # Verifica se a linha começa com "d" para processar apenas diretórios
    if [[ $line =~ ^d ]]; then
        # Extraindo o mês, dia, ano (se presente), e hora da linha
        MONTH=$(echo "$line" | awk '{print $6}')
        DAY=$(echo "$line" | awk '{print $7}')
        TIME_YEAR=$(echo "$line" | awk '{print $8}')

        # Verifica se o campo de tempo é um horário ou ano
        if [[ "$TIME_YEAR" =~ : ]]; then
            TIME="$TIME_YEAR"
            YEAR=$(date +%Y)
        else
            YEAR="$TIME_YEAR"
            TIME="00:00"
        fi

        # Converte a data extraída para o formato Unix
        FILE_DATE=$(date -d "$MONTH $DAY $YEAR $TIME" +%s 2>/dev/null)

        # Verifica se a data foi convertida corretamente
        if [ -z "$FILE_DATE" ]; then
#           echo "Erro ao processar a data na linha: $line"
            echo "0"
            continue
        fi

        # Compara a data extraída com a data limite de 7 dias
        if [ "$FILE_DATE" -lt "$LIMIT_DATE" ]; then
#           echo "A data de modificação na linha é maior que 7 dias atrás: $line"
            echo "1"
        fi
    fi
done < "$FILE"