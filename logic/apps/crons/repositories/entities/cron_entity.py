
import json
from datetime import datetime

from logic.apps.crons.models.cron_model import CronStatus, CronWork
from logic.libs.sqliteAlchemy import sqliteAlchemy
from sqlalchemy import Column, DateTime, String

Entity = sqliteAlchemy.get_entity_class()


class CronEntity(Entity):
    __tablename__ = 'CRONS'

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String)
    cron_expression = Column(String)
    status = Column(String)
    creation_date = Column(DateTime)
    work_module_repo = Column(String)
    work_module_name = Column(String)
    work_agent_type = Column(String)
    work_params = Column(String)

    def to_model(self) -> CronWork:
        return CronWork(
            name=self.name,
            cron_expression=self.cron_expression,
            work_module_repo=self.work_module_repo,
            work_module_name=self.work_module_name,
            work_agent_type=self.work_agent_type,
            id=self.id,
            creation_date=self.creation_date,
            status=CronStatus(self.status),
            work_params=json.loads(self.work_params)
        )

    @staticmethod
    def from_model(c: CronWork) -> 'CronEntity':
        return CronEntity(
            id=c.id,
            name=c.name,
            cron_expression=c.cron_expression,
            status=c.status.value,
            creation_date=c.creation_date,
            work_module_repo=c.work_module_repo,
            work_module_name=c.work_module_name,
            work_agent_type=c.work_agent_type,
            work_params=json.dumps(c.work_params)
        )
