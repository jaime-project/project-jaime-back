from dataclasses import dataclass


@dataclass
class Server():
    name: str
    host: str
    port: str
    user: str
    password: str

    def __eq__(self, o: object) -> bool:
        return self.name == o.name

    def __dict__(self):
        return {
            'name': self.name,
            'host': self.host,
            'port': self.port,
            'user': self.user,
            'password': self.password
        }
