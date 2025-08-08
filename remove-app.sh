#!/bin/bash
echo "Removing app resources ..."
docker-compose down
docker rmi flask_app
docker volume rm redis_data
docker network rm app-network

