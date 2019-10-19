from flask import Blueprint, current_app, request
from flask_restplus import Api, Resource, Namespace
from app.main.service.book_service import narrate_book

book_api = Namespace('book', description="Book endpoint")

@book_api.route('/')
class BookExample(Resource):
    def get(self):
        return "You are at book GET endpoint"

@book_api.route('/getText')
class BookInText(Resource):
    def get(self):
        text = narrate_book(request.args.get('url'))
        return text

@book_api.route('/getNarration')
class BookNarration(Resource):
    def get(self):
        path_to_audio = narrate_book(request.args.get('url'))
        response = send_file(path_to_audio, "audio/wav", attachment_filename='narration.wav', as_attachment=True)
        response.headers["x-filename"] = 'narration.wav'
        response.headers["Access-Control-Expose-Headers"] = 'x-filename'
        return response

