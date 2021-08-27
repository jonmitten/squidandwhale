#!/usr/bin/env bash
#docker build --tag python-docker .
#docker images
#docker tag python-docker:latest python-docker:v1.0.0
#docker run --publish 5000:5000 --name rest-server python-docker
#docker volume create mysql
#docker volume create mysql_config
bash ~/nuke_docker.sh
docker network create mysqlnet
docker run --rm -d -v mysql:/var/lib/mysql -v mysql_config:/etc/mysql -p 3306:3306 \
--network mysqlnet \
--name mysqldb \
-e MYSQL_ROOT_PASSWORD=p@ssw0rd1 \
mysql
docker build --tag python-docker-dev .
docker run \
--rm -d \
--network mysqlnet \
--name rest-server \
-p 5000:5000 \
python-docker-dev
