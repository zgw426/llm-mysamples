#!/bin/bash

# Dockerイメージを作る
docker build -f Dockerfile_RAG -t rag_img .

# Dockerコンテナを作成し起動する
docker run --rm --name rag_env -v $PWD/work/:/work/ -dit rag_img

# Dockerコンテナに入る
docker exec -it rag_env bash