#!/bin/sh

docker stop $(docker ps -q)
docker rm $(docker ps -q -a)
# docker rmi $(docker images -q) -f

docker build -t alpha-matting .
docker run -it -p 80:5000 alpha-matting:latest