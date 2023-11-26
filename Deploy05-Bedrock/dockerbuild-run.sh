#!/bin/bash

# Dockerイメージを作る
docker build -f Dockerfile_Bedrock -t bedrock_img .

# Dockerコンテナを作成し起動する
docker run --rm --name bedrock_env -v $PWD/work/:/work/ -dit bedrock_img

# Dockerコンテナに入る
docker exec -it bedrock_env bash