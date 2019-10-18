from flask import Blueprint, current_app, request
from flask_restplus import Api, Resource, Namespace

notes_api = Namespace('notes', description="Book endpoint")

@notes_api.route('/')
class NoteExample(Resource):
    def get(self):
        return "You are at notes GET endpoint"