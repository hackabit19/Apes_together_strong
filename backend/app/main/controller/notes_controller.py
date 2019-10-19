from flask import Blueprint, current_app, request
from flask_restplus import Api, Resource, Namespace
from app.main.service.notes_service import note_make

notes_api = Namespace('notes', description="Book endpoint")

@notes_api.route('/')
class NoteExample(Resource):
    def get(self):
        return "You are at notes GET endpoint"

@notes_api.route('/getImage')
class NotesToBoundingBoxes(Resource):
    def get(self):
        text = note_make(request.args.get('url'))

@notes_api.route('/getAudio')
class NotesToAudio(Resource):
    def get(self):
        path_to_audio = 
        text = note_make('url')
        return 

