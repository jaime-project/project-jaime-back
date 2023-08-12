from flask import Flask, request

from logic.apps.login import service
from logic.libs.rest.rest import setup

NO_LOGIN_PATHS = [
    '/',
    '/vars',
    '/api/v1/login/',
    '/api/v1/agents/',
]

NO_LOGIN_PATHS_CONTAIN = [
    '/api/v1/hooks/exec/'
]


def setup_rest(app: Flask) -> Flask:
    setup(app, [
        'logic/apps/admin/routes/admin_route.*',
        'logic/apps/*/route.*'
    ])


def setup_token(app: Flask):

    @app.before_request
    def before_request():

        if request.method != 'OPTIONS' and _need_login(request.path):

            if not 'Authorization' in request.headers or not 'Bearer ' in request.headers['Authorization']:
                return '', 401

            token = request.headers['Authorization'].replace('Bearer ', '')

            if not service.is_a_valid_token(token):
                return '', 403


def _need_login(path: str) -> bool:

    if path in NO_LOGIN_PATHS:
        return False

    for p in NO_LOGIN_PATHS_CONTAIN:
        if p in path:
            return False

    return True
