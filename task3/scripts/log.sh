#!/bin/bash
LOG_FILE="/var/log/nginx/file1.log"
CLEAR_LOG_FILE="/var/log/nginx/file2.log"
ERROR_4XX_LOG="/var/log/nginx/file3.log"
ERROR_5XX_LOG="/var/log/nginx/file4.log"

tail -n +1 -f /var/log/nginx/access.log | awk ' 
    $9 ~ /^4[0-9]{2}$/ {print $0 >> "'"$ERROR_4XX_LOG"'"}
    $9 ~ /^5[0-9]{2}$/ {print $0 >> "'"$ERROR_5XX_LOG"'"}
    {print $0 >> "'"$LOG_FILE"'"}'

#awk '!seen[$0]++' "$LOG_FILE"