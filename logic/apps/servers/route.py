from datetime import datetime
from typing import Dict

import yaml
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.responses import Response

from logic.apps.servers import service as server_service
from logic.apps.servers.model import Server

apirouter = APIRouter(prefix='/api/v1/servers', tags=['Servers'])


@apirouter.route('/', methods=['POST'])
def post(s: Dict[str, object]):
    server_service.add(
        Server(
            name=s['name'],
            host=s['host'],
            port=s['port'],
            user=s['user'],
            password=s['password']
        ))
    return JSONResponse('', 201)


@apirouter.route('/<name>', methods=['GET'])
def get(name: str):
    s = server_service.get(name)
    if not s:
        return '', 204

    return JSONResponse(s.__dict__()), 200


@apirouter.route('/', methods=['GET'])
def list_all():
    return JSONResponse(server_service.list_all()), 200


@apirouter.route('/<name>', methods=['DELETE'])
def delete(name: str):
    server_service.delete(name)
    return JSONResponse('', 200)


@apirouter.route('/all/short', methods=['GET'])
def get_all_short():
    return JSONResponse(server_service.get_all_short()), 200


@apirouter.route('/<name>/test', methods=['GET'])
def test_server(name):
    return JSONResponse(server_service.test_server(name)), 200


@apirouter.route('/<name>', methods=['PUT'])
def put(name: str, s: Dict[str, object]):

    server = Server(
        name=s['name'],
        host=s['host'],
        port=s['port'],
        user=s['user'],
        password=s['password']
    )
    server_service.modify(name, server)

    return JSONResponse('', 200)


@apirouter.route('/<name>/yamls', methods=['GET'])
def export_server(name: str):

    dict_objects = server_service.export_server(name)
    dict_yaml = str(yaml.dump(dict_objects))

    name_yaml = datetime.now().isoformat() + '.yaml'
    headers = {
        'Content-Disposition': f'attachment; filename="{name_yaml}"'}

    return Response(
        open(dict_yaml, 'rb').read(),
        media_type='application/octet-stream',
        headers=headers
    )
