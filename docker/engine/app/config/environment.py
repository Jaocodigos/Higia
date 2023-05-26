from os import environ
import logging

log = logging.getLogger("Higia." + __name__)


class Config(object):
    def __init__(self):
        self.TESTING = False
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SECRET_KEY = environ['SECRET_KEY']
        self.ADMIN_USERNAME = environ['ADMIN_USERNAME']
        self.ADMIN_PASSWORD = environ['ADMIN_PASSWORD']


class DevConfig(Config):
    def __init__(self):
        super().__init__()
        self.MYSQL_USER = environ['MYSQL_USER']
        self.MYSQL_PASSWORD = environ['MYSQL_PASSWORD']
        self.MYSQL_HOST = environ['MYSQL_HOST']
        self.MYSQL_DATABASE = environ['MYSQL_DATABASE']
        self.SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{self.MYSQL_USER}:' \
                                       f'{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}/' \
                                       f'{self.MYSQL_DATABASE}'
        self.SQLALCHEMY_ECHO = True


class TestConfig(Config):
    def __init__(self):
        super().__init__()
        self.TESTING = True
        self.SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
        self.SQLALCHEMY_ECHO = True
        self.SQLALCHEMY_TRACK_MODIFICATIONS = True


def get_flask_config():
    try:
        env = environ['FLASK_ENV'] if environ['FLASK_ENV'] else 'testing'
        if env == "development":
            return DevConfig()
        elif env == "testing":
            return TestConfig()

    except Exception as e:
        log.error(f"An error occurred while configuring application env: {e}")
        exit("Environment not provided, exiting application.")
