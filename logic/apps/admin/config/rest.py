from flask import Flask, request
from logic.apps.login.services import login_service
from logic.libs.rest.rest import setup


def setup_rest(app: Flask) -> Flask:
    setup(app, 'logic/apps/*/routes')


def setup_token(app: Flask):

    @app.before_request
    def before_request():

        if 'api/v1/login' not in request.path:

            if not 'Authorization' in request.headers:
                return '', 403

            token = request.headers['Authorization'].replace('Bearer ', '')

            if not login_service.is_a_valid_token(token):
                return '', 403
