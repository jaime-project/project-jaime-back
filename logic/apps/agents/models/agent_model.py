from dataclasses import dataclass
from uuid import UUID, uuid4
from logic.apps.admin.config.variables import Vars, get_var


@dataclass
class Agent():
    type: str
    host: str
    port: int
    id: str

    def __init__(self, id: UUID, type: str, host: str, port: int) -> None:
        self.id = id
        self.host = host
        self.port = port
        self.type = type

    def __eq__(self, o: object) -> bool:
        if not o:
            return False
        return self.id == o.id

    def get_url(self) -> str:
        protocol = 'https://' if get_var(Vars.AGENTS_HTTPS) else 'http://'
        return f'{protocol}{self.host}:{self.port}'
