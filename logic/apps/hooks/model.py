from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Dict
from uuid import uuid4

from logic.apps.jobs.model import Job


class HookStatus(Enum):
    ACTIVE = "ACTIVE"
    DESACTIVE = "DESACTIVE"


def _generate_id() -> str:
    return str(uuid4()).split("-")[4]


@dataclass
class HookJob:
    name: str
    job_module_repo: str
    job_module_name: str
    job_agent_type: str
    id: str = field(default_factory=_generate_id)
    creation_date: datetime = field(default_factory=datetime.now)
    status: HookStatus = HookStatus.ACTIVE
    job_params: dict[str, object] = field(default_factory=list)

    def to_job(self) -> Job:
        return Job(
            name=f"hookjob_{self.name}_{_generate_id()}",
            module_name=self.job_module_name,
            module_repo=self.job_module_repo,
            agent_type=self.job_agent_type,
            params=self.job_params,
        )

    def __dict__(self) -> Dict[str, object]:
        return {
            "name": self.name,
            "job_module_repo": self.job_module_repo,
            "job_module_name": self.job_module_name,
            "job_agent_type": self.job_agent_type,
            "id": self.id,
            "creation_date": self.creation_date.isoformat(),
            "status": self.status.value,
            "job_params": self.job_params,
        }
