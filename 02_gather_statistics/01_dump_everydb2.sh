#!/bin/bash
mkdir -p $UMA_PROJECT_PATH
pg_dump -U postgres -h localhost -p 5433 \
-t n_race \
-t n_uma_race \
everydb2 > $UMA_PROJECT_PATH/everydb2.sql
