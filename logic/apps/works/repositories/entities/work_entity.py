
from logic.apps.works.models.work_model import Status, WorkStatus
from logic.libs.sqliteAlchemy import sqliteAlchemy
from sqlalchemy import Column, DateTime, String

Entity = sqliteAlchemy.get_entity_class()


class WorkEntity(Entity):
    __tablename__ = 'WORKS'

    id = Column(String, primary_key=True, nullable=False)
    name = Column(String)
    module_name = Column(String)
    params = Column(String)
    agent_id = Column(String)
    status = Column(String)
    start_date = Column(DateTime)
    running_date = Column(DateTime)
    terminated_date = Column(DateTime)

    def to_model(self) -> WorkStatus:
        return WorkStatus(
            id=self.id,
            name=self.name,
            module_name=self.module_name,
            params=self.params,
            agent=self.agent_id,
            status=Status(self.status),
            start_date=self.start_date,
            running_date=self.running_date,
            terminated_date=self.terminated_date
        )

    @staticmethod
    def from_model(m: WorkStatus) -> 'WorkEntity':
        return WorkEntity(
            id=m.id,
            name=m.name,
            module_name=m.module_name,
            params=m.params,
            agent_id=m.agent.id,
            status=m.status.value,
            start_date=m.start_date,
            running_date=m.running_date,
            terminated_date=m.terminated_date
        )
