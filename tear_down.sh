#!/bin/sh

docker stop $(docker ps -a -q) # Stop all containers
docker rm $(docker ps -a -q)   # Delete all containers
docker rmi $(docker images -q) # Delete all images
docker system prune 
docker volume prune
docker image prune -a 