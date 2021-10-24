import os
import subprocess
from dataclasses import dataclass

from logic.apps.servers.models.server_model import Server


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


def sh(cmd: str, echo: bool = True) -> str:
    if echo:
        print(cmd)

    result = subprocess.getoutput(cmd)
    if echo:
        print(result)

    return result


def get_oc(server_name: str) -> "Oc":
    # TODO: hacer un servicio que busque el server y lo devuelva
    return Oc(Server(server_name))
