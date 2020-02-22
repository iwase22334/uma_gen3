#!/bin/bash
targetdir=$UMA_PROJECT_PATH

mkdir -p ${targetdir}
pg_dump -U postgres -h localhost -p 5433 \
-t n_uma \
-t n_race \
-t n_uma_race \
everydb2 > ${targetdir}/everydb2.sql

pg_dump -U postgres -h localhost -p 5433 \
-t uma_statistics_02 \
-t uma_rating_20 \
-t uma_rating_21 \
uma_processed > ${targetdir}/uma_processed.sql
