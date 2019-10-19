from flask import Blueprint, current_app, request, send_file
from flask_restplus import Api, Resource, Namespace
from app.main.service.book_service import narrate_book
import base64
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
        path_to_audio = narrate_book(request.args.get('url'), sound=True)
        response = send_file(path_to_audio, "audio/wav", attachment_filename='narration.wav', as_attachment=True)
        response.headers["x-filename"] = 'narration.wav'
        response.headers["Access-Control-Expose-Headers"] = 'x-filename'
        return response

@book_api.route('/web')
class BookNarrationWebAccess(Resource):
    def get(self):
        path_to_audio = narrate_book(request.args.get('url'), sound=True)
        with open(path_to_audio, 'rb') as audio_file:
            encoded_image = base64.b64encode(audio_file.read())
        return {'audio': encoded_image.decode('utf-8')}