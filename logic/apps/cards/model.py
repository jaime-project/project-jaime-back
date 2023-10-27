from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict
from uuid import uuid4

import yaml

from logic.apps.jobs.model import Job


def _generate_id() -> str:
    return str(uuid4()).split('-')[4]


@dataclass
class Card():
    name: str
    description: str
    color: str
    job_module_repo: str
    job_module_name: str
    job_agent_type: str
    job_default_docs: dict[str, object] = field(default_factory=dict)
    job_card_docs: str = ''
    id: str = field(default_factory=_generate_id)
    creation_date: datetime = field(default_factory=datetime.now)

    def to_job(self, params: Dict[str, object] = {}) -> Job:

        self.job_default_docs.update(params)

        return Job(
            name=f'{self.name}_{_generate_id()}',
            module_name=self.job_module_name,
            module_repo=self.job_module_repo,
            agent_type=self.job_agent_type,
            params=self.job_default_docs
        )

    def __dict__(self) -> Dict[str, object]:
        return {
            'name': self.name,
            'description': self.description,
            'color': self.color,
            'job_module_repo': self.job_module_repo,
            'job_module_name': self.job_module_name,
            'job_agent_type': self.job_agent_type,
            'job_default_docs': self.job_default_docs,
            'job_card_docs': self.job_card_docs,
            'id': self.id,
            'creation_date': self.creation_date.isoformat(),
        }
