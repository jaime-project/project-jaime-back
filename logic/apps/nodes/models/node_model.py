from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Node():
    type: str
    host: str
    port: int
    id: str = field(default=uuid4())

    def __eq__(self, o: object) -> bool:
        return self.id == o.id

    def get_url(self) -> str:
        return f'{self.host}:{self.port}'
