
import json
from pathlib import Path
from typing import List

from logic.apps.servers.errors.server_error import ServerError
from logic.apps.servers.models.server_model import Server
from logic.libs.exception.exception import AppException

_JSON_SERVER_FILE = f'{Path.home()}/.jaime/servers.json'


def add(server: Server):

    with open(_JSON_SERVER_FILE, 'r') as f:
        servers = json.loads(f.read())

    if [s for s in servers if server.name == s['name']]:
        msj = f"El server con nombre {server.name} ya existe"
        raise AppException(ServerError.SERVER_ALREADY_EXISTS_ERROR, msj)

    servers.append({
        "name": server.name,
        "url": server.url,
        "token": server.token,
        "version": server.version
    })

    with open(_JSON_SERVER_FILE, 'w') as f:
        f.write(json.dumps(servers))


def get(name: str) -> Server:

    with open(_JSON_SERVER_FILE, 'r') as f:
        servers = json.loads(f.read())

    for s in servers:
        if s['name'] == name:
            return Server(
                name=s['name'],
                url=s['url'],
                token=s['token'],
                version=s['version']
            )

    return None


def list_all() -> List[str]:

    with open(_JSON_SERVER_FILE, 'r') as f:
        servers = json.loads(f.read())

    return [
        s['name']
        for s in servers
    ]


def delete(name: str):

    with open(_JSON_SERVER_FILE, 'r') as f:
        servers = json.loads(f.read())

    servers_new = [
        s for s in servers
        if s['name'] != name
    ]

    if len(servers_new) == len(servers):
        msj = f"El server con nombre {name} no existe"
        raise AppException(ServerError.SERVER_NOT_EXISTS_ERROR, msj)

    with open(_JSON_SERVER_FILE, 'w') as f:
        f.write(json.dumps(servers_new))


def get_path() -> str:

    global _JSON_SERVER_FILE
    return _JSON_SERVER_FILE
