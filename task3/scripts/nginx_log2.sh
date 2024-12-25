#!/bin/bash

LOG_FILE="/var/log/nginx/file1.log"
CLEAN_LOG_FILE="/var/log/nginx/file2.log"
ERROR_4XX_LOG="/var/log/nginx/file3.log"
ERROR_5XX_LOG="/var/log/nginx/file4.log"
MAX_SIZE=3072

while true; do

    for file in "$LOG_FILE" "$CLEAN_LOG_FILE" "$ERROR_4XX_LOG" "$ERROR_5XX_LOG"; do
        if [[ ! -f $file ]]; then
            touch "$file"
        fi
    done

    if [[ $(stat --printf="%s" "$LOG_FILE") -gt $MAX_SIZE ]]; then
        LINE_COUNT=$(wc -l < "$LOG_FILE")
        echo "$(date): Cleared $LINE_COUNT lines from $LOG_FILE" >> "$CLEAN_LOG_FILE"
        echo "$(date): Log file exceeded 300 KB, clearing contents." > "$LOG_FILE"
    fi

    tail -n 20 /var/log/nginx/access.log >> "$LOG_FILE"

    awk '$9 ~ /^4[0-9]{2}$/ {print $0 >> "'$ERROR_4XX_LOG'"} $9 ~ /^5[0-9]{2}$/ {print $0 >> "'$ERROR_5XX_LOG'"}' /var/log/nginx/access.log
   
    sleep 5
done
