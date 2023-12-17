from dataclasses import dataclass


@dataclass
class Cluster():
    name: str
    url: str
    token: str

    def __eq__(self, o: object) -> bool:
        return self.name == o.name

    def __dict__(self):
        return {
            'name': self.name,
            'url': self.url,
            'token': self.token,
        }
