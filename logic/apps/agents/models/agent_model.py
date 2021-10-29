from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Agent():
    type: str
    host: str
    port: int
    id: str

    def __init__(self, type: str, host: str, port: int) -> None:
        self.type = type
        self.host = host
        self.port = port
        self.id = str(uuid4()).split("-")[4]

    def __eq__(self, o: object) -> bool:
        return self.id == o.id

    def get_url(self) -> str:
        return f'{self.host}:{self.port}'
