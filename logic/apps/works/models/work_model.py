from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict

from logic.apps.agents.models.agent_model import Agent


class Status(Enum):
    RUNNING = 'RUNNING'
    TERMINATED = 'TERMINATED'
    READY = 'READY'
    ERROR = 'ERROR'


@dataclass
class WorkStatus():

    id: str
    name: str
    module_name: str
    module_repo: str
    params: Dict[str, object]
    agent: Agent
    status: Status
    start_date: datetime
    running_date: datetime
    terminated_date: datetime

    def __init__(self, id: str, params: Dict[str, object]) -> "WorkStatus":
        self.id = id
        self.name = params['name']
        self.module_name = params['module']['name']
        self.module_repo = params['module']['repo']
        self.params = params
        self.agent = None
        self.status = Status.READY
        self.start_date = datetime.now()
        self.running_date = None
        self.terminated_date = None

    def finish(self):
        self.terminated_date = datetime.now()
