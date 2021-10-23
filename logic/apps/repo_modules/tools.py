from http import server
import os
import subprocess
from dataclasses import dataclass

from logic.apps.servers.models.server_model import Server


@dataclass
class Tools():
    working_dir: str
    log_file: str

    def __init__(self, working_dir: str) -> "Tools":
        self.working_dir = working_dir
        self.log_file = os.path.join(self.working_dir, "logs.log")

    def path(self, file: str) -> str:
        return os.path.join(self.working_dir, file)

    def log(self, msj: str):
        if not os.path.exists(self.log_file):
            self._sh(f"> {self.log_file}")

        self._sh(f"echo {msj} >> {self.log_file}")

    def _sh(self, cmd: str) -> str:
        return subprocess.getoutput(cmd)

    def sh(self, cmd: str, echo: bool = True) -> str:
        if echo:
            self.log(cmd)

        result = self._sh(cmd)
        if echo:
            self.log(result)

        return result

    def get_oc(self, server_name: str) -> "Oc":
        # TODO: hacer un servicio que busque el server y lo devuelva
        return Oc(Server(server_name), self)


@dataclass
class Oc():
    server: Server
    tools: Tools

    def __init__(self, server: Server, tools: Tools) -> "Oc":
        self.server = server
        self.tools = tools

    def login(self) -> str:
        return self.server.login()

    def exec(self, cmd: str, echo: bool = True) -> str:
        final_cmd = f"{self.server.binary_name()} {cmd}"
        return self.tools.sh(final_cmd, echo)
