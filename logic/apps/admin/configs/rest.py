from typing import Any, Callable

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from logic.apps.login import service as login_service
from logic.libs.rest.rest import setup


def setup_rest(app: FastAPI):
    setup(app, 'logic/apps/admin/routes')
    setup(app, 'logic/apps/*/route.*')


def setup_token(app: FastAPI):

    @app.middleware("http")
    def before_request(request: Request, call_next: Callable):

        no_login_paths = [
            '/api/v1/login/',
            '/',
            '/vars',
            '/api/v1/agents/',
        ]

        response = call_next(request)

        if request.method != 'OPTIONS' and str(request.url).replace(str(request.base_url), '') not in no_login_paths:


            if not 'Authorization' in request.headers or not 'Bearer ' in request.headers['Authorization']:
                # response.status_code = 401
                return response

            token = request.headers['Authorization'].replace('Bearer ', '')

            if not login_service.is_a_valid_token(token):
                # response.status_code = 403
                return response

        return response
