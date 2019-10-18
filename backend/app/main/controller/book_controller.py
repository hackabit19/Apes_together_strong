from flask import Blueprint, current_app, request
from flask_restplus import Api, Resource, Namespace

book_api = Namespace('book', description="Book endpoint")

@book_api.route('/')
class BookExample(Resource):
    def get(self):
        return "You are at book GET endpoint"