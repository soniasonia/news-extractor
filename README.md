# simple-page

Page that allows you to read news without ads. 
Simply provide website URL and click "Extract" to scrap the selected page and receive a pure list of article titles and their direct urls.
You can also save your extract to DB.

## Architecture
This app is built as a Docker application so it can be easily run and deployed on different environments.
It is managed with docker-compose and it consists of 2 containers (services):
- **app** - developed in Flask, Python framework for web application
- **mongo** - Mongo database used by Flask app

## Development
For debug purposes you can run Flask application locally 
```python
python manage.py runserver
```
You can also run mongo-express container (database client) together with mongo container to preview your data
- **mongo** - Mongo database used by Flask app
- **mongo-express** - Mongo DB client

## Configuration
- **.env** - environment variables for local Flask app run, including
 ```FLASK_ENV=dev```
- **docker.env** - environment variables for Docker dev run, including
  ```FLASK_ENV=docker```
- **prod.env** - environment variables for Docker production run, including
```FLASK_ENV=prod```
