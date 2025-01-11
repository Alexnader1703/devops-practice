#!/bin/bash

LOG_FILE="/var/log/nginx/file1.log"
CLEAR_LOG_FILE="/var/log/nginx/file2.log"
ERROR_4XX_LOG="/var/log/nginx/file3.log"
ERROR_5XX_LOG="/var/log/nginx/file4.log"
MAX_SIZE=30720

while true; do

    for file in "$LOG_FILE" "$CLEAR_LOG_FILE" "$ERROR_4XX_LOG" "$ERROR_5XX_LOG"; do
        if [[ ! -f $file ]]; then
            touch "$file"
        fi
    done

    if [ $(stat -c %s $LOG_FILE) -ge $MAX_SIZE ]; then
        COUNT_LINE=$(wc -l < $LOG_FILE)
        echo "" > "$LOG_FILE"
        echo "$(date): Cleared $COUNT_LINE lines from $LOG_FILE" >> "$CLEAR_LOG_FILE"
    fi

    tail -n 20 /var/log/nginx/access.log  >> "$LOG_FILE"
    awk '!seen[$0]++' '$LOG_FILE' > "$LOG_FILE"

    awk '$9 ~ /^4[0-9]{2}$/ {print $0 >> "'$ERROR_4XX_LOG'"} $9 ~ /^5[0-9]{2}$/ {print $0 >> "'$ERROR_5XX_LOG'"}' /var/log/nginx/access.log
    awk '!seen[$0]++' '$ERROR_4XX_LOG' > "$ERROR_4XX_LOG"
    awk '!seen[$0]++' '$ERROR_5XX_LOG' > "$ERROR_5XX_LOG"
    sleep 5
done

