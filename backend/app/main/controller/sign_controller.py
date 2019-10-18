from flask import Blueprint, current_app, request, render_template, Response, make_response
from flask_restplus import Api, Resource, Namespace

from app.main.service.sign_service import gen
from camera import Camera

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

@sign_api.route('/camera')
class VideoFeed(Resource):
    def get(self):
        return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


