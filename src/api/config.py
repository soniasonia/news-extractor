# more configuration options here http://flask.pocoo.org/docs/1.0/config/

import os
class Config:
    """
    Base Configuration
    """

    # CHANGE SECRET_KEY!! I would use sha256 to generate one and set this as an environment variable
    # Exmaple to retrieve env variable `SECRET_KEY`: os.environ.get("SECRET_KEY")
    SECRET_KEY = "testkey"
    LOG_FILE = "api.log"  # where logs are outputted to


class DevelopmentConfig(Config):
    """
    Requires the environment variable `FLASK_ENV=dev`
    """
    MONGO_URI = os.environ.get("MONGO_URI")
    DEBUG = True


class ProductionConfig(Config):
    """
    Requires the environment variable `FLASK_ENV=prod`
    """
    MONGO_URI = os.environ.get("MONGO_URI")
    DEBUG = False



# way to map the value of `FLASK_ENV` to a configuration
config = {"dev": DevelopmentConfig, "prod": ProductionConfig}