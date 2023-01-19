from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict
from uuid import uuid4

from logic.apps.jobs.model import Job


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
    id: str = field(default_factory=_generate_id)
    creation_date: datetime = field(default_factory=datetime.now)
    status: CronStatus = CronStatus.ACTIVE
    work_params: Dict[str, object] = field(default_factory={})

    def to_workStatus(self) -> Job:

        return Job(
            name=f'cronjob_{self.name}_{_generate_id()}',
            module_name=self.work_module_name,
            module_repo=self.work_module_repo,
            agent_type=self.work_agent_type,
            params=self.work_params
        )
