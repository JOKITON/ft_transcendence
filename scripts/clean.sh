#!/bin/bash
docker rm $(docker ps -qa)

docker rmi $(docker images -q)

docker volume rm $(docker volume ls -q)

docker system prune --force