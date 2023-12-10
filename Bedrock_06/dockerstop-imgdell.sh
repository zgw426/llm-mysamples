#!/bin/bash

# Dockerコンテナを停止する
docker stop rag_env

# Dockerイメージを削除する
docker image rm rag_img