from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from logic.apps.agents.models.agent_model import Agent


class Status(Enum):
    RUNNING = 'RUNNING'
    TERMINATED = 'TERMINATED'
    READY = 'READY'


@dataclass
class WorkStatus():

    id = str
    agent: Agent
    status: Status
    init_date: datetime
    end_date: datetime

    def __init__(self, id: str, agent: Agent = None, status: Status = Status.READY, init_date: datetime = datetime.now, end_date: datetime = None) -> "WorkStatus":
        self.id = id
        self.agent = agent
        self.status = status
        self.init_date = init_date
        self.end_date = end_date

    def finish(self):
        self.end_date = datetime.now()
