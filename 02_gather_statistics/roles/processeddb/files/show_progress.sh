#!/bin/bash
watch -n 0.5 "psql -h localhost -d uma_processed -c 'select count(*) from uma_statistics_02;'"
