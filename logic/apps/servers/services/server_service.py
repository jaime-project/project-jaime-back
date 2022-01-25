
from typing import Dict, List

import requests
import yaml
from logic.apps.agents.errors.agent_error import AgentError
from logic.apps.agents.services import agent_service
from logic.apps.servers.errors.server_error import ServerError
from logic.apps.servers.models.server_model import Server, ServerType
from logic.apps.servers.repositories import server_repository
from logic.libs.exception.exception import AppException


def add(server: Server):

    if server_repository.exist(server.name):
        msj = f"El server con nombre {server.name} ya existe"
        raise AppException(ServerError.SERVER_ALREADY_EXISTS_ERROR, msj)

    server_repository.add(server)


def get(name: str) -> Server:

    if not server_repository.exist(name):
        return None

    return server_repository.get(name)


def list_all() -> List[str]:

    return [
        s.name
        for s in server_repository.get_all()
    ]


def get_all() -> List[str]:
    return server_repository.get_all()


def get_all_short() -> List[Dict[str, str]]:

    return [
        {
            "name": s.name,
            "type": s.type.value,
            "url": s.url
        }
        for s in server_repository.get_all()
    ]


def delete(name: str):

    if not server_repository.exist(name):
        msj = f"El server con nombre {name} no existe"
        raise AppException(ServerError.SERVER_NOT_EXISTS_ERROR, msj)

    server_repository.delete(name)


def list_types() -> str:
    return [e.value for e in ServerType]


def test_server(name: str) -> Dict[str, str]:

    server = get(name)
    agents = agent_service.get_by_type(server.type)
    if not agents:
        raise AppException(AgentError.AGENT_NOT_EXIST_ERROR,
                           "No hay agentes para la tarea")

    url = agents[0].get_url()
    json = {
        'url': server.url,
        'token': server.token
    }
    return requests.post(url=f'{url}/api/v1/jaime/servers/test', json=json).json()


def modify(name: str, server: Server):
    delete(name)
    add(server)
