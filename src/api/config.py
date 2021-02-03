# more configuration options here http://flask.pocoo.org/docs/1.0/config/
import os


class Config:
    """
    Base Configuration
    """

    # CHANGE SECRET_KEY!! use sha256 and set this as an environment variable
    # os.environ.get("SECRET_KEY")
    SECRET_KEY = "testkey"
    MONGO_URI = os.environ.get("MONGO_URI")


class DevelopmentConfig(Config):
    """
    Requires the environment variable `FLASK_ENV=dev`
    """
    LOG_FILE = "api.log"  # where logs are outputted to
    DEBUG = True


class TestConfig(Config):
    """
    Requires the environment variable `FLASK_ENV=test`
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    Requires the environment variable `FLASK_ENV=prod`
    """
    LOG_FILE = "api.log"  # where logs are outputted to
    DEBUG = False


# way to map the value of `FLASK_ENV` to a configuration
config = {"dev": DevelopmentConfig,
          "test": TestConfig,
          "prod": ProductionConfig}
