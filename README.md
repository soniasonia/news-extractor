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

## Run for development
For development and debug purposes you can run Flask application locally (outside Docker).

1. Create Python virtual env and install the requirements
    - example for Linux
    ```
    python3 -m venv venv
    source venv/bin/activate
    pip install -r backend/requirements.txt
    ```
2. Run Docker service for mongo DB and DB client
    ```
    sudo docker-compose up mongo
    sudo docker-compose up mongo-express
    ```
3. Create DB user
   - login to Mongo DB using initial creds
   ```
   sudo docker exec -it [container] mongo admin --username root --password secret
   ```
   - create database and user dedicated to the application
   ```
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
## Run in Docker (dev)
Database and user are created automatically while mongo DB initialization, using mongo-init.js.
1. Simply run Docker services
    ```
    sudo docker-compose up mongo
    sudo docker-compose up mongo-express
    sudo-docker-compose up app
    ```
    
 ## Run in Docker (prod)
1. Update mongo-init.js
    ```
    db.auth('admin-user', 'admin-pass')

    db = db.getSiblingDB('simple-app')

    db.createUser(
            {
                user: "user",
                pwd: "pass",
                roles: [
                    {
                        role: "readWrite",
                        db: "simple-app"
                    }
                ]
            }
    );
    ```
2. Update docker-compose.yml
    ```
    services:
     app:
      environment:
       MONGO_URI: valid-mongo-uri
       FLASK_ENV: prod
       
     mongo:
      environment:
        MONGO_INITDB_ROOT_USERNAME: admin-user
        MONGO_INITDB_ROOT_PASSWORD: admin-pass
        MONGO_INITDB_DATABASE: admin
    ```

3. Run application
    ```
    sudo docker-compose up mongo
    sudo-docker-compose up app
    ```
