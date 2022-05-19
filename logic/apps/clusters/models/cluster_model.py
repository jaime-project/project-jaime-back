from dataclasses import dataclass
from enum import Enum


class ClusterType(Enum):
    OPENSHIFT = 'OPENSHIFT'


@dataclass
class Cluster():
    name: str
    url: str
    token: str
    type: ClusterType
    version: str

    def __init__(self, name: str, url: str, token: str, version: str, type: ClusterType) -> "Cluster":
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
