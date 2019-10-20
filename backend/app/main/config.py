import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig(Config):
    DEBUG = True
    HOST = '127.0.0.1'
    PORT = 3000
    # database URI goes here


config_by_name = dict(
    dev=DevelopmentConfig
)