from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from uuid import uuid4


class Status(Enum):
    NOT_SEEN = 'NOT_SEEN'
    SEEN = 'SEEN'


def _generate_id() -> str:
    return str(uuid4()).split('-')[4]


@dataclass
class Message():
    title: str
    subject: str
    body: str
    job: str
    files: list[str] = field(default_factory=[])
    date: datetime = field(default_factory=datetime.now)
    status: Status = Status.NOT_SEEN
    id: str = field(default_factory=_generate_id)

    def __eq__(self, o: object) -> bool:
        return self.id == o.id

    def __dict__(self):
        return {
            'id': self.id,
            'title': self.title,
            'job': self.job,
            'subject': self.subject,
            'date': self.date.isoformat(),
            'body': self.body,
            'files': self.files,
            'status': self.status.value,
        }
