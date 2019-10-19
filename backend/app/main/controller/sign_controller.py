from flask import Blueprint, current_app, request, render_template, Response, make_response, send_file
from flask_restplus import Api, Resource, Namespace
import base64
from app.main.service.sign_service import gen
from camera import Camera
from app.main.utils.toSignTranslator.main import func

sign_api = Namespace('sign', description="Sign endpoint")

@sign_api.route('/')
class SignExample(Resource):
    def get(self):
        return "You are at sign GET endpoint"

@sign_api.route('/video')
class VideoTemp(Resource):
    def get(self):
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template('video.html'), 200, headers)

@sign_api.route('/tosign')
class ToSign(Resource):
    def get(self):
        vid_path = func(request.args.get('url'))
        response = send_file(vid_path, "video/avi", attachment_filename='tosign.avi', as_attachment=True)
        response.headers["x-filename"] = 'tosign.avi'
        response.headers["Access-Control-Expose-Headers"] = 'x-filename'
        return response

@sign_api.route('/web')
class ToSignWeb(Resource):
    def get(self):
        vid_path = func(request.args.get('url'))
        with open(vid_path, 'rb') as audio_file:
            encoded_audio = base64.b64encode(audio_file.read())
        return {'video': encoded_audio.decode('utf-8')}

@sign_api.route('/camera')
class VideoFeed(Resource):
    def get(self):
        return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


