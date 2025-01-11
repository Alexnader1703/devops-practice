#!/bin/bash

psql "host=rc1a-grt37oou2mre9ab6.mdb.yandexcloud.net \
    port=6432 \
    sslmode=verify-full \
    dbname=jundb \
    user=trainee8 \
    target_session_attrs=read-write"

psql "host=rc1a-grt37oou2mre9ab6.mdb.yandexcloud.net \
    port=6432 \
    sslmode=verify-full \
    dbname=jundb \
    user=trainee8 \
    target_session_attrs=read-write" < backup.sql


PGSSLMODE=verify-full pg_dump -h rc1a-grt37oou2mre9ab6.mdb.yandexcloud.net   -p 6432   -U trainee8   -d jundb > backup.sql

pg_dump -h rc1a-grt37oou2mre9ab6.mdb.yandexcloud.net \
  -p 6432 \
  -U trainee8 \
  --ssl-mode=verify-full \
  -d jundb > backup.sql