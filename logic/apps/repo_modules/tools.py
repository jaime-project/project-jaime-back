import subprocess
from dataclasses import dataclass

from logic.apps.servers.models.server_model import Server
from logic.apps.servers.services import server_service


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
    return Oc(server_service.get(server_name))
