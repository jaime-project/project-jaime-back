
import json

from logic.apps.agents.models.agent_model import Agent
from logic.apps.works.models.work_model import Status, Work
from logic.libs.sqliteAlchemy import sqliteAlchemy
from sqlalchemy import Column, DateTime, String

Entity = sqliteAlchemy.get_entity_class()


class WorkEntity(Entity):
    __tablename__ = 'WORKS'

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String)
    module_name = Column(String)
    module_repo = Column(String)
    params = Column(String)
    agent = Column(String)
    agent_type = Column(String)
    status = Column(String)
    start_date = Column(DateTime)
    running_date = Column(DateTime)
    terminated_date = Column(DateTime)

    def to_model(self) -> Work:

        agent = None
        if self.agent:
            a = json.loads(self.agent)
            agent = Agent(
                id=a['id'],
                type=a['type'],
                host=a['host'],
                port=a['port']
            )

        return Work(
            name=self.name,
            module_name=self.module_name,
            module_repo=self.module_repo,
            agent=agent,
            agent_type=self.agent_type,
            id=self.id,
            status=Status(self.status),
            params=json.loads(self.params),
            start_date=self.start_date,
            running_date=self.running_date,
            terminated_date=self.terminated_date
        )

    @staticmethod
    def from_model(m: Work) -> 'WorkEntity':
        return WorkEntity(
            id=m.id,
            name=m.name,
            module_name=m.module_name,
            module_repo=m.module_repo,
            agent_type=m.agent_type,
            params=json.dumps(m.params),
            agent=json.dumps(m.agent.__dict__()) if m.agent else None,
            status=m.status.value,
            start_date=m.start_date,
            running_date=m.running_date,
            terminated_date=m.terminated_date
        )
