#!/bin/bash

docker build -t surneco-warehouse_setup:latest .
docker container stop surneco-warehouse >> /dev/null 2<&1
docker container rm surneco-warehouse >> /dev/null 2<&1
docker run -t -d -p 8080:8080 --name surneco-warehouse surneco-warehouse_setup:latest

declare -a DEL_IMGS=`docker image ls | grep '<none>' | awk '{print$3}'`

echo -e "\nRemoving unused docker images..."

for i in ${DEL_IMGS}; do
    echo $i
    docker image rm $i
done 

echo -e '\n\nNOW ONLINE!!'