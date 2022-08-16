from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict
from uuid import uuid4

from logic.apps.agents.models.agent_model import Agent


class Status(Enum):
    RUNNING = 'RUNNING'
    READY = 'READY'
    ERROR = 'ERROR'
    SUCCESS = 'SUCCESS'
    CANCEL = 'CANCEL'


def _generate_id() -> str:
    return str(uuid4()).split('-')[4]


@dataclass
class Work():

    name: str
    module_name: str
    module_repo: str
    agent_type: str
    agent: Agent = None
    id: str = _generate_id()
    status: Status = Status.READY
    params: Dict[str, object] = field(default_factory={})
    start_date: datetime = datetime.now()
    running_date: datetime = None
    terminated_date: datetime = None

    # def __init__(self, id: str = _generate_id(), params: Dict[str, object] = {}) -> "WorkStatus":
    #     self.id = id
    #     self.name = params['name']
    #     self.module_name = params['module']['name']
    #     self.module_repo = params['module']['repo']
    #     self.agent = None
    #     self.agent_type = params['agent']['type']
    #     self.status = Status.READY
    #     self.start_date = datetime.now()
    #     self.running_date = None
    #     self.terminated_date = None

    #     final_params = params.copy()
    #     final_params.pop('name')
    #     final_params.pop('module')
    #     final_params.pop('agent')

    #     self.params = final_params

    def finish(self):
        self.terminated_date = datetime.now()
