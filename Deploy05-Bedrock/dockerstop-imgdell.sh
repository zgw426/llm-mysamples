#!/bin/bash

# Dockerコンテナを停止する
docker stop bedrock_env

# Dockerイメージを削除する
docker image rm bedrock_img