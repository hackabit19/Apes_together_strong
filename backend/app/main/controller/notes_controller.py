from flask import Blueprint, current_app, request, send_file
from flask_restplus import Api, Resource, Namespace
from app.main.service.notes_service import note_make
import base64
notes_api = Namespace('notes', description="Book endpoint")

@notes_api.route('/')
class NoteExample(Resource):
    def get(self):
        return "You are at notes GET endpoint"

@notes_api.route('/getImage')
class NotesToBoundingBoxes(Resource):
    def get(self):
        img_path = note_make(just_img=True)
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

@notes_api.route('/download')
class Download(Resource):
    def get(self):
        response = send_file(request.args.get('url'), "image/jpg", attachment_filename='labelled.jpg', as_attachment=True)
        response.headers["x-filename"] = 'labelled.jpg'
        response.headers["Access-Control-Expose-Headers"] = 'x-filename'
        return response

@notes_api.route('/web')
class NotesToAudioWeb(Resource):
    def get(self):
        aud_path = note_make(request.args.get('url'))
        with open(aud_path, 'rb', encoding='utf-8') as audio_file:
            encoded_audio = base64.b64encode(audio_file.read())
        img_path  = note_make(just_img=True)
        print(img_path)
        return {'audio': encoded_audio.decode('utf-8', errors='replace'), 'image': img_path}

