from flask import Blueprint, current_app, request
from flask_restplus import Api, Resource, Namespace

sign_api = Namespace('sign', description="Sign endpoint")

@sign_api.route('/')
class SignExample(Resource):
    def get(self):
        return "You are at sign GET endpoint"