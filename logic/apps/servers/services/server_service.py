
from pathlib import Path
from typing import Dict, List

import requests
import yaml
from logic.apps.agents.errors.agent_error import AgentError
from logic.apps.agents.services import agent_service
from logic.apps.servers.errors.server_error import ServerError
from logic.apps.servers.models.server_model import Server, ServerType
from logic.libs.exception.exception import AppException

_YAML_SERVER_FILE = f'{Path.home()}/.jaime/servers.yaml'


def add(server: Server):

    servers = _get_servers_from_file()

    if server in servers:
        msj = f"El server con nombre {server.name} ya existe"
        raise AppException(ServerError.SERVER_ALREADY_EXISTS_ERROR, msj)

    _save_server_in_file(server)


def get(name: str) -> Server:

    servers = _get_servers_from_file()

    for s in servers:
        if s.name == name:
            return s

    return None


def list_all() -> List[str]:

    return [
        s.name
        for s in _get_servers_from_file()
    ]


def get_all_short() -> List[Dict[str, str]]:

    return [
        {
            "name": s.name,
            "type": s.type.value,
            "url": s.url
        }
        for s in _get_servers_from_file()
    ]


def delete(name: str):

    servers = _get_servers_from_file()

    servers_dict = [
        s.__dict__()
        for s in servers
        if s.name != name
    ]

    if len(servers_dict) == len(servers):
        msj = f"El server con nombre {name} no existe"
        raise AppException(ServerError.SERVER_NOT_EXISTS_ERROR, msj)

    with open(_YAML_SERVER_FILE, 'w') as f:
        f.write(yaml.dump(servers_dict))


def get_path() -> str:

    global _YAML_SERVER_FILE
    return _YAML_SERVER_FILE


def _get_servers_from_file() -> List[Server]:

    with open(_YAML_SERVER_FILE, 'r') as f:
        servers_dict = yaml.load(f.read(), Loader=yaml.FullLoader)

    if not servers_dict:
        return []

    return [
        Server(
            name=s['name'],
            url=s['url'],
            token=s['token'],
            version=s['version'],
            type=ServerType(s['type'])
        )
        for s in servers_dict
    ]


def _save_server_in_file(server: Server):

    servers_dict = [
        s.__dict__()
        for s in _get_servers_from_file()
    ]

    servers_dict.append({
        "name": server.name,
        "url": server.url,
        "token": server.token,
        "version": server.version,
        "type": server.type.value
    })

    with open(_YAML_SERVER_FILE, 'w') as f:
        f.write(yaml.dump(servers_dict))


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
