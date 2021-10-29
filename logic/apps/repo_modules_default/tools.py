import subprocess
import sys
from dataclasses import dataclass
from subprocess import PIPE, Popen
from typing import Dict

import yaml
from logic.apps.filesystem.services.workingdir_service import get
from logic.apps.servers.errors.server_error import ServerError
from logic.apps.servers.models.server_model import Server
from logic.apps.servers.services import server_service
from logic.libs.exception.exception import AppException


@dataclass
class Oc():
    server: Server

    def __init__(self, server: Server) -> "Oc":
        self.server = server

    def login(self) -> str:
        return self.server.login()

    def exec(self, cmd: str, echo: bool = True) -> str:
        final_cmd = f"{self.server.binary_name()} {cmd}"
        return sh(final_cmd, echo)

    def binary_name(self) -> str:
        return self.server.binary_name()


def sh(cmd: str, echo: bool = True) -> str:

    if echo:
        print(cmd)
        result = subprocess.run(cmd, shell=True, stdout=PIPE, close_fds=False)
    if echo and result.stdout:
        print(result.stdout.decode())

    return result.stdout.decode() if result.stdout else ""


def get_oc(server_name: str) -> "Oc":
    server = server_service.get(server_name)
    if not server:
        msj = f'No existe el server de nombre {server_name}'
        raise AppException(ServerError.SERVER_NOT_EXISTS_ERROR, msj)
    return Oc(server_service.get(server_name))


def get_params() -> Dict[str, object]:
    with open(sys.argv[1], 'r') as f:
        return yaml.load(f.read())
