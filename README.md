Documentation (22ug2-0584)

** Deployment Requirements **
Docker = Docker is a software platform that allows you to build, test, and deploy applications quickly.

Docker Compose =  Docker Compose is a tool that helps you define and share multi-container applications. 

Dockerfile = A Dockerfile is a text file containing instructions for building your source code. 
 
requirements.txt =  requirements.txt is a file that contains a list of packages or libraries needed to work on a project that can all be installed with the file.

Flask = Flask is a micro web framework written in Python. 

Redis = Redis is an open-source, in-memory data structure store that is used as a database, cache, and message broker.


** Application Description **
This is a simple web application built using Flask and Redis.
this web application shows that, every time the page is refreshed, the total number of visits is increased and displayed. When the containers are stopped or restarted, the visit count remains unchanged since Redis uses a **persistent volume**.


** Network and Volume Details **
In Docker Compose, a network refers to a communication layer that allows the containers of the services defined in the docker-compose.yaml file to talk to each other.

NetworkT
his application use bridge network named app-network (dirver:bridge).This enables communication between two services names insted of IP addresses.

Volume (redis_data)
A named Docker volume used by the redis_db container to store Redis data files. This ensures the visit count is preserved across container restarts or re-deployments.

/*
networks:
  app-network:
    driver: bridge

volumes:
  redis_data:
*/


** Container Configuration **

flask_app
- Custom-built Docker image from `app/`
- Port - 5000
- This depends on 'redis_db' for storing the visit counter

redis_db
- port - 6379
- Official `redis:7-alpine` image


** Container List **
flask_app - Web server listening on port 5000
redis_db - Key-value store with persistent volume


** Instructions **
./prepare-app.sh - Prepares the Docker network for communication.

./start-app.sh - Starts both flask_app and redis_db containers and makes the application available at http://localhost:5000

./stop-app.sh - Stops all running containers without deleting volumes, preserving the Redis data.

./remove-app.sh - Removes containers, images, networks, and volumes created for the application.


** Example Workflow **
./prepare-app.sh --> ./start-app.sh --> visit count 1 --> ./stop-app.sh --> ./start-app.sh --> visit count 2 --> ./remove-app.sh

|1. Preparing app 
|2. App is available at: http://localhost:5000
|3. Visit Count: 1 ( curl http://localhost:5000)
|4. Stopping app
|5. App is available at: http://localhost:5000
|6. Visit Count: 2 (curl http://localhost:5000)
v7. Removing app resources




































