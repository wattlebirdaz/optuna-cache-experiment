#!/bin/sh

echo "Prepare PostgreSQL 14.3 Server using Docker."
docker stop optuna-postgres

set -e
docker run \
  -d \
  --rm \
  -p 5432:5432 \
  --platform linux/x86_64 \
  -e POSTGRES_USER=root \
  -e POSTGRES_DB=optuna \
  -e POSTGRES_PASSWORD=root \
  --name optuna-postgres-withoutcache \
  postgres:14.3

docker run \
  -d \
  --rm \
  -p 5433:5432 \
  --platform linux/x86_64 \
  -e POSTGRES_USER=root \
  -e POSTGRES_DB=optuna \
  -e POSTGRES_PASSWORD=root \
  --name optuna-postgres-withcache \
  postgres:14.3

sleep 10