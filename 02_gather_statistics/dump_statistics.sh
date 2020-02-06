#!/bin/bash

mkdir -p ${UMA_PROJECT_PATH}
pg_dump \
-t uma_statistics_02 \
uma_processed > ${UMA_PROJECT_PATH}/statistics_02.sql
