from os import environ


class Config(object):
    """Base configuration."""

    DB_HOST = "localhost"
    DB_USER = "postgres"
    DB_PASS = "cabj1211"
    DB_NAME = "DSSD14"
    SECRET_KEY = 'esto-es-una-clave-muy-secreta'

    @staticmethod
    def configure(app):
        # Implement this method to do further configuration on your app.
        pass


class ProductionConfig(Config):
    """Production configuration."""

    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ("postgresql://postgres:cabj1211@localhost:5432/DSSD14")


class DevelopmentConfig(Config):
    """Development configuration."""

    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ("postgresql://postgres:cabj1211@localhost:5432/DSSD14")


class TestingConfig(Config):
    """Testing configuration."""

    TESTING = True
    DB_HOST = environ.get("DB_HOST", "localhost")
    DB_USER = environ.get("DB_USER", "MY_DB_USER")
    DB_PASS = environ.get("DB_PASS", "MY_DB_PASS")
    DB_NAME = environ.get("DB_NAME", "MY_DB_NAME")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = ("postgresql://postgres:cabj1211@localhost:5432/DSSD14")

config = dict(
    development=DevelopmentConfig, test=TestingConfig, production=ProductionConfig
)

## More information
# https://flask.palletsprojects.com/en/2.0.x/config/