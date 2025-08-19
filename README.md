Documentation (22ug2-0584)

** Deployment Requirements **
Docker = Docker is a software platform that allows you to build, test, and deploy applications quickly.

Docker Compose =  Docker Compose is a tool that helps you define and share multi-container applications. 

Dockerfile = A Dockerfile is a text file containing instructions for building your source code. 
 
requirements.txt =  requirements.txt is a file that contains a list of packages or libraries needed to work on a project that can all be installed with the file.

Flask = Flask is a micro web framework written in Python. 

Redis = Redis is an open-source, in-memory data structure store that is used as a database, cache, and message broker.

--------------------------------------------------------------

** Application Description **
This is a simple Flask + Redis web application.This webpage displays song lists; the user can "like" a particular song, which then gets stored in Redis.

Since Redis uses a persistent volume, the liked songs stay saved even after the containers are stopped or restarted. This is really wanting to show container communication and persistent state across redeployments.

---------------------------------------------------------------

** Network and Volume Details **
In Docker Compose, a network refers to a communication layer that allows the containers of the services defined in the docker-compose.yaml file to talk to each other.

Network
In Docker Compose, a network allows containers to communicate using service names instead of IP addresses.
networks:
  app-network:
    driver: bridge

Volume (redis_data)
A named Docker volume used by the redis_db container to store Redis data files. This ensures the visit count is preserved across container restarts or re-deployments.

volumes:
  redis_data:

---------------------------------------------------------------

** Container Configuration **

flask_app
- Custom-built Docker image from the local Dockerfile
- Port - 5000
- This depends on 'redis_db' for storing liked songs

redis_db
- port - 6379
- Uses official `redis:7-alpine` image
- Stores data in the named volume redis_data

---------------------------------------------------------------

** Container List **
flask_app - Web server listening on port 5000
redis_db - Key-value store with persistent volume

---------------------------------------------------------------

** Instructions **
./prepare-app.sh - Prepares the Docker network for communication.

./start-app.sh - Starts both flask_app and redis_db containers and makes the application available at http://localhost:5000

./stop-app.sh - Stops all running containers without deleting volumes, preserving the Redis data.

./remove-app.sh - Removes containers, images, networks, and volumes created for the application.

---------------------------------------------------------------

** Example Workflow **

1. ./prepare-app.sh --> Create resources and build images
2. ./start-app.sh --> Start the application
3. App is available at http://localhost:5000
4. Do changes in application (Liked some songs)
5. Refresh or Restart containers to check liked song remain
6. ./stop-app.sh --> Stop containers but preserve data
7. ./start-app.sh --> Start again and verify liked songs persist
8. ./remove-app.sh --> Remove everything

--------------------------------------------------------------

** Originality and References **

[1]“Volumes,” Docker Documentation, 2025. https://docs.docker.com/reference/compose-file/volumes/ (accessed Aug. 08, 2025). 
[2]GeeksforGeeks, “Flask (Creating first simple application),” GeeksforGeeks, Oct. 23, 2017. https://www.geeksforgeeks.org/python/flask-creating-first-simple-application/ (accessed Aug. 08, 2025). 
[3]“Networks,” Docker Documentation, 2025. https://docs.docker.com/reference/compose-file/networks/ (accessed Aug. 08, 2025). ‌‌ ‌
































