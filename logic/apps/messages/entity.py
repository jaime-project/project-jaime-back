import json
from datetime import datetime

from sqlalchemy import Column, String, Text

from logic.apps.messages.model import Message, Status
from logic.libs.sqliteAlchemy import sqliteAlchemy

Entity = sqliteAlchemy.get_entity_class()


class MessageEntity(Entity):
    __tablename__ = 'MESSAGES'

    id = Column(String(30), primary_key=True, nullable=False)
    title = Column(String(60))
    subject = Column(String(60))
    date = Column(String(255))
    body = Column(Text)
    files = Column(Text)
    status = Column(String(30))
    job = Column(String(30))

    def to_model(self) -> Message:
        return Message(
            id=self.id,
            title=self.title,
            subject=self.subject,
            date=datetime.fromisoformat(self.date),
            body=self.body,
            files=json.loads(self.files),
            status=Status(self.status),
            job=self.job
        )

    @staticmethod
    def from_model(m: Message) -> 'MessageEntity':
        return MessageEntity(
            id=m.id,
            title=m.title,
            subject=m.subject,
            date=m.date,
            body=m.body,
            files=json.dumps(m.files),
            status=m.status.value,
            job=m.job
        )
