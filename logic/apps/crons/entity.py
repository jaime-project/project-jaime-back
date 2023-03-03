
import json

from sqlalchemy import Column, DateTime, String, Text

from logic.apps.crons.model import CronStatus, CronJob
from logic.libs.sqliteAlchemy import sqliteAlchemy

Entity = sqliteAlchemy.get_entity_class()


class CronEntity(Entity):
    __tablename__ = 'CRONS'

    id = Column(String(30), primary_key=True, nullable=False)
    name = Column(String(60))
    cron_expression = Column(String(10))
    status = Column(String(30))
    creation_date = Column(DateTime)
    job_module_repo = Column(String(255))
    job_module_name = Column(String(255))
    job_agent_type = Column(String(30))
    job_params = Column(Text)

    def to_model(self) -> CronJob:
        return CronJob(
            name=self.name,
            cron_expression=self.cron_expression,
            job_module_repo=self.job_module_repo,
            job_module_name=self.job_module_name,
            job_agent_type=self.job_agent_type,
            id=self.id,
            creation_date=self.creation_date,
            status=CronStatus(self.status),
            job_params=json.loads(self.job_params)
        )

    @staticmethod
    def from_model(c: CronJob) -> 'CronEntity':
        return CronEntity(
            id=c.id,
            name=c.name,
            cron_expression=c.cron_expression,
            status=c.status.value,
            creation_date=c.creation_date,
            job_module_repo=c.job_module_repo,
            job_module_name=c.job_module_name,
            job_agent_type=c.job_agent_type,
            job_params=json.dumps(c.job_params)
        )
