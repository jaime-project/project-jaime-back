from flask import Flask, request

from logic.apps.login import service
from logic.libs.rest.rest import setup

NO_LOGIN_PATHS = [
    '/api/v1/login/',
    '/',
    '/api/v1/agents/',
    '/vars',
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

        no_login_paths = [
            '/api/v1/login/',
            '/',
            '/api/v1/agents/',
            '/vars',
            '/api/v1/hooks/exec/'
        ]

        if request.method != 'OPTIONS' and not _is_a_no_login_path(request.path):

            if not 'Authorization' in request.headers or not 'Bearer ' in request.headers['Authorization']:
                return '', 401

            token = request.headers['Authorization'].replace('Bearer ', '')

            if not service.is_a_valid_token(token):
                return '', 403


def _is_a_no_login_path(path: str) -> bool:

    for no_login_path in NO_LOGIN_PATHS:
        if no_login_path in path:
            return True

    return False
