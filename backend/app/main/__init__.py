from logging import getLogger

from flask import Flask
from flask_cors import CORS
from app.main.config import config_by_name

LOG = getLogger(__name__)

LOG.info('configured logger!')


def create_app(config_name):
    app = Flask(__name__, template_folder="../static/templates", static_folder="../static")
    app.config.from_object(config_by_name[config_name])
    LOG.info('app loaded with configuration!')

    app.app_context().push()
    LOG.info('application context pushed')

    CORS(app)
    LOG.info("Flask-CORS set up succesfully!")

    return app