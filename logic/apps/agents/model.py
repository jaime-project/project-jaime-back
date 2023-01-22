from dataclasses import dataclass
from enum import Enum
from uuid import UUID

from logic.apps.admin.configs.variables import Vars, get_var


class AgentStatus(Enum):
    WORKING = 'WORKING'
    READY = 'READY'


@dataclass
class Agent():
    type: str
    host: str
    port: int
    id: UUID
    status: AgentStatus

    def __init__(self, id: UUID, type: str, host: str, port: int, status: AgentStatus = AgentStatus.READY) -> None:
        self.id = id
        self.host = host
        self.port = port
        self.type = type
        self.status = status

    def __dict__(self):
        return {
            'type': self.type,
            'host': self.host,
            'port': self.port,
            'id': self.id,
            'status': self.status.value
        }

    def __eq__(self, o: object) -> bool:
        if not o:
            return False
        return self.id == o.id

    def get_url(self) -> str:
        protocol = 'https://' if get_var(Vars.AGENTS_HTTPS) else 'http://'
        return f'{protocol}{self.host}:{self.port}'
