#!/bin/bash
echo "Preparing app ..."
docker volume create redis_data
docker network create app-network || echo "Network already exists"
docker build -t flask_app ./app

