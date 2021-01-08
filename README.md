# simple-page

Page that allows you to read news without ads. 
Simply provide website URL and click "Extract" to scrap the selected page and receive a pure list of article titles and their direct urls.
You can also save your extract to DB.

## Architecture
This app is built as a Docker application so it can be easily run and deployed on different environments.
It is managed with docker-compose and it consists of 3 containers (services):
- **app** - developed in Flask, Python framework for web application
- **mongo** - Mongo database used by Flask app

#### DEVELOPMENT
For debug purposes you can run Flask application locally and use the following containers 
```python
python manage.py runserver
``` 

- **mongo** - Mongo database used by Flask app
- **mongo-express** - Mongo DB client


## Continuous Integration
This project uses Travis CI to automatically test code changes with every git push:
- runs flake8 for checking code syntax against PEP 8 (Style Guide for Python Code)