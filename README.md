# simple-page

Page that allows you to read news without ads. 
Simply provide website URL and click "Extract" to scrap the selected page and receive a pure list of article titles and their direct urls.
![Screenshot](./docs/pics/start_page.png)

You can also save your extract to DB.
![Screenshot](./docs/pics/result_page.png)

## Architecture
This app is built as a Docker application so it can be easily run and deployed on different environments.
It is managed with docker-compose and it consists of 2 containers (services):
- **app** - developed in Flask, Python framework for web application
- **mongo** - Mongo database used by Flask app

## Development
For development and debug purposes you can run Flask application locally (outside Docker) 
1. Run Docker service for mongo DB and DB client
    ```
    sudo docker-compose up mongo
    sudo docker-compose up mongo-express
    ```
2. Create database and user
   ```
   sudo docker exec -it [container] mongo
   db.getSiblingDB('simple-app-db').createUser({user:'user', pwd:'pass', 
   roles:[{role:'readWrite',db:'simple-app-db'}]})
    ```
4. Define environment variables
    ```
    FLASK_ENV=env
    MONGO_URI=mongodb://user:pass@localhost:27017/simple-app-db
    ```
5. Run application
    ```python
    python manage.py runserver
    ```
