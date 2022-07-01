#!/usr/bin/env bash

wait-for-it "${EXAMPLE_DB_HOST:-example-database}":5432 -s -t 180 \
&& pytest --cov
