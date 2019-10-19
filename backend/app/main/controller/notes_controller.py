from flask import Blueprint, current_app, request, send_file
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
        img_path = note_make(request.args.get('url'), just_img=True)
        response = send_file(img_path, "image/jpg", attachment_filename='notes_output_img.jpg', as_attachment=True)
        response.headers["x-filename"] = 'notes_output_img.jpg'
        response.headers["Access-Control-Expose-Headers"] = 'x-filename'
        return response

# call this before to create the image
@notes_api.route('/getAudio')
class NotesToAudio(Resource):
    def get(self):
        aud_path = note_make(request.args.get('url'))
        response = send_file(aud_path, "audio/wav", attachment_filename='notes_audio.wav', as_attachment=True)
        response.headers["x-filename"] = 'notes_audio.wav'
        response.headers["Access-Control-Expose-Headers"] = 'x-filename'
        return response

