from typing import Dict, List

from logic.apps.servers.errors.server_error import ServerError
from logic.apps.servers.models.server_model import Server
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


def get_all() -> List[Server]:
    return server_repository.get_all()


def get_all_short() -> List[Dict[str, str]]:

    return [
        {
            "name": s.name,
            "host": s.host,
            "port": s.port
        }
        for s in server_repository.get_all()
    ]


def delete(name: str):

    if not server_repository.exist(name):
        msj = f"El server con nombre {name} no existe"
        raise AppException(ServerError.SERVER_NOT_EXISTS_ERROR, msj)

    server_repository.delete(name)


def test_server(name: str) -> Dict[str, str]:
    any


def modify(name: str, server: Server):
    delete(name)
    add(server)
