from dataclasses import dataclass
from enum import Enum


class ServerType(Enum):
    OPENSHIFT = 'OPENSHIFT'
    KUBERNETES = 'KUBERNETES'


@dataclass
class Server():
    name: str
    url: str
    token: str
    type: ServerType
    version: str

    def __init__(self, name: str, url: str, token: str, version: str, type: ServerType) -> "Server":
        self.name = name
        self.url = url
        self.token = token
        self.type = type
        self.version = version

    def __eq__(self, o: object) -> bool:
        return self.name == o.name

    def __dict__(self):
        return {
            'name': self.name,
            'url': self.url,
            'token': self.token,
            'type': self.type.value,
            'version': self.version
        }
