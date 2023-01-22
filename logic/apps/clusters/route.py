import ntpath
from datetime import datetime
from typing import Dict

import yaml
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.responses import Response

from logic.apps.clusters import service
from logic.apps.clusters.model import Cluster

apirouter = APIRouter(prefix='/api/v1/clusters', tags=['Clusters'])


@apirouter.route('/', methods=['POST'])
def post(s: Dict[str, object]):
    service.add(Cluster(
        name=s['name'],
        url=s['url'],
        token=s['token'],
        version=s['version'],
        type=s['type']
    ))
    return JSONResponse('', 201)


@apirouter.route('/<name>', methods=['GET'])
def get(name: str):
    s = service.get(name)
    if not s:
        return '', 204

    return JSONResponse(s.__dict__()), 200


@apirouter.route('/', methods=['GET'])
def list_all():

    return JSONResponse(service.list_all()), 200


@apirouter.route('/<name>', methods=['DELETE'])
def delete(name: str):
    service.delete(name)
    return JSONResponse('', 200)


@apirouter.route('/all/short', methods=['GET'])
def get_all_short():
    return JSONResponse(service.get_all_short()), 200


@apirouter.route('/<name>/test', methods=['GET'])
def test_cluster(name):
    return JSONResponse(service.test_cluster(name)), 200


@apirouter.route('/<name>', methods=['PUT'])
def modify_server(name: str, s: Dict[str, object]):

    server = Cluster(
        name=s['name'],
        url=s['url'],
        token=s['token'],
        version=s['version'],
        type=s['type']
    )
    service.modify(name, server)

    return JSONResponse('', 200)


@apirouter.route('/<name>/yamls', methods=['GET'])
def export_cluster(name: str):

    dict_objects = service.export_cluster(name)
    dict_yaml = str(yaml.dump(dict_objects))

    name_yaml = datetime.now().isoformat() + '.yaml'
    headers = {
        'Content-Disposition': f'attachment; filename="{ntpath.basename(name_yaml)}"'}

    return Response(
        open(dict_yaml, 'rb').read(),
        media_type='application/octet-stream',
        headers=headers
    )
