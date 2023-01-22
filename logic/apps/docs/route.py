import yaml
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.responses import Response

from logic.apps.docs import service

apirouter = APIRouter(prefix='/api/v1/repos/<repo>/docs', tags=['Docs'])


@apirouter.route('/<name>', methods=['POST'])
def post(name: str, repo: str, content: bytes):
    service.add(name, content.decode('utf8'), repo)
    return JSONResponse('', 201)


@apirouter.route('/<name>', methods=['GET'])
def get(name: str, repo: str):
    content = service.get(name, repo)
    return Response(content, mimetype='text/plain', status=200)


@apirouter.route('/<name>/yaml', methods=['GET'])
def get_yaml(name: str, repo: str):
    content = service.get(name, repo)

    dict_yaml = yaml.load(content)
    if 'yaml' in dict_yaml:
        dict_yaml = dict_yaml['yaml']
        return Response(yaml.dump(dict_yaml), mimetype='text/plain', status=200)

    return Response('', mimetype='text/plain', status=200)


@apirouter.route('/', methods=['GET'])
def list_all(repo: str):
    return JSONResponse(service.list_all(repo)), 200


@apirouter.route('/<name>', methods=['DELETE'])
def delete(name: str, repo: str):
    service.delete(name, repo)
    return JSONResponse('', 200)


@apirouter.route('/<name>', methods=['PUT'])
def modify(name: str, repo: str, content: bytes):
    service.modify(name, content.decode('utf8'), repo)
    return JSONResponse('', 200)
