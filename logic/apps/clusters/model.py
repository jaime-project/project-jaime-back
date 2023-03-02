from dataclasses import dataclass


@dataclass
class Cluster():
    name: str
    url: str
    token: str
    type: str

    def __init__(self, name: str, url: str, token: str, type: str) -> "Cluster":
        self.name = name
        self.url = url
        self.token = token
        self.type = type

    def __eq__(self, o: object) -> bool:
        return self.name == o.name

    def __dict__(self):
        return {
            'name': self.name,
            'url': self.url,
            'token': self.token,
            'type': self.type,
        }
