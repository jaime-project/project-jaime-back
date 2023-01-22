from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.responses import Response

from logic.apps.modules import service

apirouter = APIRouter(prefix='/api/v1/repos/<repo>/modules', tags=['Modules'])


@apirouter.route('/<name>', methods=['POST'])
def post(name: str, repo: str, content: bytes):
    service.add(name, content.decode('utf8'), repo)
    return JSONResponse(JSONResponse('', 201))


@apirouter.route('/<name>', methods=['GET'])
def get(name: str, repo: str):
    content = service.get(name, repo)
    return Response(content, media_type='text/plain', status_code=200)


@apirouter.route('/', methods=['GET'])
def list_all(repo: str):
    return JSONResponse(service.list_all(repo), 200)


@apirouter.route('/<name>', methods=['DELETE'])
def delete(name: str, repo: str):
    service.delete(name, repo)
    return JSONResponse(JSONResponse('', 200))


@apirouter.route('/<name>', methods=['PUT'])
def modify(name: str, repo: str, content: bytes):
    service.modify(name, content.decode('utf8'), repo)
    return JSONResponse('', 200)
