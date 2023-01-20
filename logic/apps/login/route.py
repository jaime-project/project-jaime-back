from typing import Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from logic.apps.login import service
from logic.libs.exception.exception import AppException

apirouter = APIRouter(prefix='/api/v1/login', tags=['Login'])


@apirouter.route('/', methods=['POST'])
def login(j: Dict[str, object]):

    try:
        token = service.login(j['user'], j['pass'])
        return token, 200

    except AppException as app:
        return JSONResponse(app.to_json()), 403


@apirouter.route('/refresh', methods=['GET'])
def refresh():
    return '', 200
