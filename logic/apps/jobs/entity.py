import json

from sqlalchemy import Column, DateTime, String, Text

from logic.apps.agents.model import Agent
from logic.apps.jobs.model import Job, Status
from logic.libs.sqliteAlchemy import sqliteAlchemy

Entity = sqliteAlchemy.get_entity_class()


class JobEntity(Entity):
    __tablename__ = 'JOBS'

    id = Column(String(30), primary_key=True, nullable=False)
    name = Column(String(60))
    module_name = Column(String(60))
    module_repo = Column(String(60))
    params = Column(Text)
    agent = Column(String(255))
    agent_type = Column(String(255))
    status = Column(String(30))
    start_date = Column(DateTime)
    running_date = Column(DateTime)
    terminated_date = Column(DateTime)

    def to_model(self) -> Job:

        agent = None
        if self.agent:
            a = json.loads(self.agent)
            agent = Agent(
                id=a['id'],
                type=a['type'],
                host=a['host'],
                port=a['port']
            )

        return Job(
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
    def from_model(m: Job) -> 'JobEntity':
        return JobEntity(
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
