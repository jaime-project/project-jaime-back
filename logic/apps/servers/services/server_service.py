from typing import Dict, List

import paramiko
from logic.apps.servers.errors.server_error import ServerError
from logic.apps.servers.models.server_model import Server
from logic.apps.servers.repositories import server_repository
from logic.libs.exception.exception import AppException
from sqlalchemy import false, true


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

    server = get(name)
    if not server:
        msj = f"El server con nombre {name} no existe"
        raise AppException(ServerError.SERVER_NOT_EXISTS_ERROR, msj)

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(
            hostname=server.host,
            username=server.user,
            password=server.password,
            port=int(server.port)
        )
        out = None
        _, out, _ = ssh.exec_command('ls')

        return {
            'success': out != None,
            'text': ''
        }
    except Exception as e:
        return {
            'success': False,
            'text': str(e)
        }


def modify(name: str, server: Server):
    delete(name)
    add(server)


def export_server(server_name: str) -> Dict[str, List[Dict[str, str]]]:

    objects = {}

    objects['servers'] = [
        o.__dict__()
        for o in get_all()
        if o.name == server_name
    ]

    return objects
