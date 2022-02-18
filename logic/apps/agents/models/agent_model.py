from dataclasses import dataclass
from uuid import UUID, uuid4
from logic.apps.admin.config.variables import Vars, get_var
from logic.apps.clusters.models.cluster_model import ClusterType
from enum import Enum


class AgentStatus(Enum):
    WORKING = 'WORKING'
    READY = 'READY'


@dataclass
class Agent():
    type: ClusterType
    host: str
    port: int
    id: str
    status: AgentStatus

    def __init__(self, id: UUID, type: ClusterType, host: str, port: int, status: AgentStatus = AgentStatus.READY) -> None:
        self.id = id
        self.host = host
        self.port = port
        self.type = type
        self.status = status

    def __dict__(self):
        return {
            'type': self.type.value,
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
