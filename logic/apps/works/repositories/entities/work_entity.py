
import json

from logic.apps.agents.models.agent_model import Agent
from logic.apps.clusters.models.cluster_model import ClusterType
from logic.apps.works.models.work_model import Status, WorkStatus
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
        w.status = Status(self.status)
        w.start_date = self.start_date
        w.running_date = self.running_date
        w.terminated_date = self.terminated_date

        if self.agent:
            a = json.loads(self.agent)
            w.agent = Agent(
                id=a['id'],
                type=ClusterType(a['type']),
                host=a['host'],
                port=a['port']
            )

        return w

    @staticmethod
    def from_model(m: WorkStatus) -> 'WorkEntity':
        return WorkEntity(
            id=m.id,
            name=m.name,
            module_name=m.module_name,
            module_repo=m.module_repo,
            params=json.dumps(m.params),
            agent=json.dumps(m.agent.__dict__()) if m.agent else None,
            status=m.status.value,
            start_date=m.start_date,
            running_date=m.running_date,
            terminated_date=m.terminated_date
        )
