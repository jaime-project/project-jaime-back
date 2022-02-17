
import json
from flask import jsonify
from logic.apps.works.models.work_model import Status, WorkStatus
from logic.libs.sqliteAlchemy import sqliteAlchemy
from sqlalchemy import Column, DateTime, String
from logic.apps.agents.services import agent_service

Entity = sqliteAlchemy.get_entity_class()


class WorkEntity(Entity):
    __tablename__ = 'WORKS'

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String)
    module_name = Column(String)
    module_repo = Column(String)
    params = Column(String)
    agent_id = Column(String)
    status = Column(String)
    start_date = Column(DateTime)
    running_date = Column(DateTime)
    terminated_date = Column(DateTime)

    def to_model(self) -> WorkStatus:
        w = WorkStatus(
            id=self.id,
            params=json.loads(self.params)
        )
        w.name = self.name
        w.module_name = self.module_name
        w.module_repo = self.module_repo
        w.agent = agent_service.get(self.agent_id) if self.agent_id else None
        w.status = Status(self.status)
        w.start_date = self.start_date
        w.running_date = self.running_date
        w.terminated_date = self.terminated_date

        return w

    @ staticmethod
    def from_model(m: WorkStatus) -> 'WorkEntity':
        return WorkEntity(
            id=m.id,
            name=m.name,
            module_name=m.module_name,
            module_repo=m.module_repo,
            params=json.dumps(m.params),
            agent_id=m.agent.id if m.agent != None else None,
            status=m.status.value,
            start_date=m.start_date,
            running_date=m.running_date,
            terminated_date=m.terminated_date
        )
