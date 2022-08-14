from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict
from uuid import uuid4
from logic.apps.works.models.work_model import WorkStatus


class CronStatus(Enum):
    ACTIVE = 'ACTIVE'
    DESACTIVE = 'DESACTIVE'


def _generate_id() -> str:
    return str(uuid4()).split('-')[4]


@dataclass
class CronWork():
    name: str
    cron_expression: str
    work_module_repo: str
    work_module_name: str
    work_agent_type: str
    id: str = _generate_id()
    creation_date: datetime = datetime.now()
    status: CronStatus = CronStatus.ACTIVE
    work_params: Dict[str, object] = field(default_factory={})

    def to_workStatus(self) -> WorkStatus:

        params = self.work_params.copy()

        params['agent'] = {}
        params['agent']['type'] = self.work_agent_type

        params['module'] = {}
        params['module']['repo'] = self.work_module_repo
        params['module']['name'] = self.work_module_name

        params['name'] = f'cronjob_{self.name}_{_generate_id()}'

        return WorkStatus(params=params)
