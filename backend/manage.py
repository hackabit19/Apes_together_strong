"""
Entrypoint of the application.
"""

import os
import unittest
from logging import getLogger

from flask import current_app
from flask_script import Manager

from app import blueprint
from app.main import create_app

LOG = getLogger(__name__)

app = create_app(os.getenv('FLASK_ENV') or 'dev')

app.register_blueprint(blueprint)
LOG.info('blueprints registered')

manager = Manager(app)

@manager.command
def run():
    """Run the flask app."""
    LOG.info('initiating app...')
    app.run(host=current_app.config['HOST'],
            port=current_app.config['PORT'], debug=current_app.config['DEBUG'])

if __name__ == '__main__':
    manager.run()