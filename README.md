Technologies Used:
- Python 3.8
- Flask
- Mongo
- Redis
- Docker
- DotEnv
- Virtual Environment
- Pycharm
- MongoDB Compass
- Postman
- MacOS


Check for sure Makefile


Installation:
- Start with setup MongoDB
- Pull Mongodb 
- _`docker pull mongo`_
- Check is it installed
- _`docker image ls`_
- Run mongodb as daemon mode
- _`~~docker run -d -p 27017:27017 mongo:latest~~`_
- Check is mongodb up
- _`docker ps`_

- Then setup Redis
- Pull Redis 
- _`docker pull redis`_
- Check is it installed
- _`docker image ls`_
- Run redis as daemon mode
- _`~~docker run -d -p 6379:6379 redis~~`_
- Check is redis up
- _`docker ps`_
- For redis-cli change container id
- docker exec -it 518c818c83c4 redis-cli