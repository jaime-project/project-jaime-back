import subprocess
import sys
from dataclasses import dataclass
from subprocess import PIPE
from typing import Dict

import yaml

_SERVER_FILE_NAME = 'servers.yaml'


@dataclass
class Server():
    name: str
    url: str
    token: str
    version: str

    def __init__(self, name: str, url: str, token: str, version: str) -> "Server":
        self.name = name
        self.url = url
        self.token = token
        self.version = version

    def __eq__(self, o: object) -> bool:
        return self.name == o.name

    def login(self) -> str:
        short_version = self.version.split(".")[0]

        if short_version == "3":
            cmd = f"{self.binary_name()} login {self.url} --token={self.token}"

        if short_version == "4":
            cmd = f"{self.binary_name()} login --server={self.url} --token={self.token}"

        sh(cmd)

    def binary_name(self) -> str:
        short_version = self.version.split(".")[0]

        if short_version == "3":
            return "oc"

        return "oc"


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
        result = subprocess.getoutput(cmd)
    if echo and result:
        print(result)

    return result if result else ""


def get_oc(server_name: str) -> "Oc":

    with open(_SERVER_FILE_NAME, 'r') as f:
        servers_dict = yaml.load(f.read(), Loader=yaml.FullLoader)

    for s in servers_dict:

        if s['name'] == server_name:
            server = Server(
                name=s['name'],
                url=s['url'],
                token=s['token'],
                version=s['version']
            )
            return Oc(server)

    if not server_name in servers_dict:
        raise Exception(f'No existe el server de nombre {server_name}')


def get_params() -> Dict[str, object]:
    with open(sys.argv[1], 'r') as f:
        return yaml.load(f.read())
