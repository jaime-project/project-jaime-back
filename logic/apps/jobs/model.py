import os
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict
from uuid import uuid4

from logic.apps.agents.model import Agent


class Status(Enum):
    RUNNING = 'RUNNING'
    READY = 'READY'
    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'
    CANCEL = 'CANCEL'


def _generate_id() -> str:
    return str(uuid4()).split('-')[4]


@dataclass
class Job():

    name: str
    module_name: str
    module_repo: str
    agent_type: str
    agent: Agent = None
    id: str = field(default_factory=_generate_id)
    status: Status = Status.READY
    params: Dict[str, object] = field(default_factory={})
    start_date: datetime = field(default_factory=datetime.now)
    running_date: datetime = None
    terminated_date: datetime = None

    def finish(self):
        self.terminated_date = datetime.now()
