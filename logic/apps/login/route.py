from typing import Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from logic.apps.login import service
from logic.apps.login.model import Login
from logic.libs.exception.exception import AppException

apirouter = APIRouter(prefix='/api/v1/login', tags=['Login'])


@apirouter.post('/')
def login(login: Login):

    try:
        token = service.login(login.user, login.password)
        return JSONResponse(token, 200)

    except AppException as app:
        return JSONResponse(app.to_json(), 403)


@apirouter.get('/refresh')
def refresh():
    return JSONResponse('', 200)
