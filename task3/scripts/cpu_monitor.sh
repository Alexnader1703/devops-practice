#!/bin/bash
while true; do
    echo $(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')% > /var/www/html/cpu_usage.txt
    sleep 1
done