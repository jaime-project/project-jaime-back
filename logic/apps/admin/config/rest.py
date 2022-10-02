from flask import Flask, request
from logic.apps.login.services import login_service
from logic.libs.rest.rest import setup
from flask_cors import CORS


def setup_rest(app: Flask) -> Flask:
    setup(app, 'logic/apps/*/routes')


def setup_token(app: Flask):

    @app.before_request
    def before_request():

        no_login_paths = [
            '/api/v1/login/',
            '/',
            '/api/v1/agents/'
        ]

        if request.method != 'OPTIONS' and request.path not in no_login_paths:

            if not 'Authorization' in request.headers or not 'Bearer ' in request.headers['Authorization']:
                return '', 403

            token = request.headers['Authorization'].replace('Bearer ', '')

            if not login_service.is_a_valid_token(token):
                return '', 403
