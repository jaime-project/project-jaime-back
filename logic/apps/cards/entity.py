import json

from sqlalchemy import Column, DateTime, String, Text

from logic.apps.cards.model import Card
from logic.libs.sqliteAlchemy import sqliteAlchemy

Entity = sqliteAlchemy.get_entity_class()


class CardEntity(Entity):
    __tablename__ = 'CARDS'

    id = Column(String(30), primary_key=True, nullable=False)
    name = Column(String(60))
    description = Column(Text)
    color = Column(String(30))
    job_module_repo = Column(String(100))
    job_module_name = Column(String(100))
    job_agent_type = Column(String(30))
    job_default_docs = Column(Text)
    job_card_docs = Column(Text)
    creation_date = Column(DateTime)

    def to_model(self) -> Card:
        return Card(
            name=self.name,
            description=self.description,
            color=self.color,
            job_module_repo=self.job_module_repo,
            job_module_name=self.job_module_name,
            job_agent_type=self.job_agent_type,
            id=self.id,
            creation_date=self.creation_date,
            job_default_docs=json.loads(self.job_default_docs),
            job_card_docs=self.job_card_docs
        )

    @staticmethod
    def from_model(c: Card) -> 'CardEntity':
        return CardEntity(
            id=c.id,
            name=c.name,
            color=c.color,
            description=c.description,
            creation_date=c.creation_date,
            job_module_repo=c.job_module_repo,
            job_module_name=c.job_module_name,
            job_agent_type=c.job_agent_type,
            job_default_docs=json.dumps(c.job_default_docs),
            job_card_docs=c.job_card_docs,
        )
