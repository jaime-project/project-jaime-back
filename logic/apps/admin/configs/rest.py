from flask import Flask, request

from logic.apps.login import service
from logic.libs.rest.rest import setup


def setup_rest(app: Flask) -> Flask:
    setup(app, [
        'logic/apps/admin/routes/admin_route.*',
        'logic/apps/*/route.*'
    ])


def setup_token(app: Flask):
    @app.before_request
    def before_request():

        no_login_paths = [
            '/api/v1/login/',
            '/',
            '/api/v1/agents/',
            '/vars'
        ]

        if request.method != 'OPTIONS' and request.path not in no_login_paths:

            if not 'Authorization' in request.headers or not 'Bearer ' in request.headers['Authorization']:
                return '', 401

            token = request.headers['Authorization'].replace('Bearer ', '')

            if not service.is_a_valid_token(token):
                return '', 403