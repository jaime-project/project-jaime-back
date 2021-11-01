
from pathlib import Path
from typing import Dict, List

import yaml
from logic.apps.servers.errors.server_error import ServerError
from logic.apps.servers.models.server_model import Server
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


def delete(name: str):

    servers = _get_servers_from_file()

    servers_new = [
        s for s in servers
        if s.name != name
    ]

    if len(servers_new) == len(servers):
        msj = f"El server con nombre {name} no existe"
        raise AppException(ServerError.SERVER_NOT_EXISTS_ERROR, msj)

    with open(_YAML_SERVER_FILE, 'w') as f:
        f.write(yaml.dump(servers_new))


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
            version=s['version']
        )
        for s in servers_dict
    ]


def _save_server_in_file(server: Server):

    servers_dict = [
        s.__dict__
        for s in _get_servers_from_file()
    ]

    servers_dict.append({
        "name": server.name,
        "url": server.url,
        "token": server.token,
        "version": server.version
    })

    with open(_YAML_SERVER_FILE, 'w') as f:
        f.write(yaml.dump(servers_dict))
