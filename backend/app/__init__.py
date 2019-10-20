from flask import Blueprint
from flask_restplus import Api

from app.main.controller.book_controller import book_api as book_ns
from app.main.controller.notes_controller import notes_api as notes_ns
from app.main.controller.sign_controller import sign_api as sign_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='Flask-RESTPlus common backend for Hack-A-BIT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

api.add_namespace(book_ns, path='/book')
api.add_namespace(notes_ns, path='/notes')
api.add_namespace(sign_ns, path='/sign')
