#!/bin/sh

echo "Prepare MySQL 8.0 Server using Docker."
docker stop optuna-mysql

docker run \
  -d \
  --rm \
  -p 3306:3306 \
  --mount type=volume,src=mysql,dst=/etc/mysql/conf.d \
  -e MYSQL_USER=optuna \
  -e MYSQL_DATABASE=optuna \
  -e MYSQL_PASSWORD=password \
  -e MYSQL_ALLOW_EMPTY_PASSWORD=yes \
  --name optuna-mysql-withoutcache \
  mysql:8.0

docker run \
  -d \
  --rm \
  -p 3307:3306 \
  --mount type=volume,src=mysql,dst=/etc/mysql/conf.d \
  -e MYSQL_USER=optuna \
  -e MYSQL_DATABASE=optuna \
  -e MYSQL_PASSWORD=password \
  -e MYSQL_ALLOW_EMPTY_PASSWORD=yes \
  --name optuna-mysql-withcache \
  mysql:8.0

sleep 10