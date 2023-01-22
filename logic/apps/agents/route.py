from typing import Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from logic.apps.agents import service
from logic.apps.agents.model import Agent
from logic.apps.login import service as login_service

apirouter = APIRouter(prefix='/api/v1/agents', tags=['Agents'])


@apirouter.route('/', methods=['POST'])
def post(j: Dict[str, object]):
    n = Agent(
        id=j['id'],
        host=j['host'],
        port=j['port'],
        type=j['type']
    )

    service.add(n)
    token = login_service.get_token()

    return JSONResponse(token, 201)


@apirouter.route('/<id>', methods=['DELETE'])
def delete(id: str):

    service.delete(id)
    return JSONResponse('', 200)


@apirouter.route('/', methods=['GET'])
def list_all():

    agents = service.list_all()
    result = [
        {
            'id': a.id,
            'host': a.host,
            'port': a.port,
            'type': a.type,
            'status': a.status.value,
        }
        for a in agents
    ]

    return JSONResponse(result), 200


@apirouter.route('/all/short', methods=['GET'])
def get_all_short():

    result = service.get_all_short()
    return JSONResponse(result), 200


@apirouter.route('/<id>', methods=['GET'])
def get(id: str):

    n = service.get(id)
    if not n:
        return '', 204

    result = {
        "type": n.type,
        "host": n.host,
        "port": n.port,
        "id": n.id,
        'status': n.status.value,
    }

    return JSONResponse(result), 200


@apirouter.route('/types', methods=['GET'])
def list_types():
    return JSONResponse(service.list_types()), 200
