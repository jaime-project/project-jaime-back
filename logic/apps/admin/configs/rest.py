from typing import Callable

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from starlette.requests import Request

from logic.apps.login import service as login_service
from logic.libs.rest.rest import setup


def setup_rest(app: FastAPI):
    setup(app, [
        'logic/apps/admin/routes/route.*',
        'logic/apps/*/route.*'
    ])


def setup_token(app: FastAPI):

    @app.middleware("http")
    async def before_request(request: Request, call_next: Callable):
        no_login_paths = [
            'api/v1/login/',
            '',
            'docs',
            'vars',
            'api/v1/agents/',
            'openapi.json'
        ]

        path = str(request.url).replace(str(request.base_url), '')

        if request.method != 'OPTIONS' and path not in no_login_paths:

            if not 'Authorization' in request.headers or not 'Bearer ' in request.headers['Authorization']:
                return JSONResponse('', 401)

            token = request.headers['Authorization'].replace('Bearer ', '')

            if not login_service.is_a_valid_token(token):
                return JSONResponse('', 403)

        response = await call_next(request)
        return response
