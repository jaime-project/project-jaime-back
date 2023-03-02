from sqlalchemy import Column, String, Text

from logic.apps.servers.model import Server
from logic.libs.sqliteAlchemy import sqliteAlchemy

Entity = sqliteAlchemy.get_entity_class()


class ServerEntity(Entity):
    __tablename__ = 'SERVERS'

    name = Column(String(60), primary_key=True, nullable=False)
    host = Column(String(255))
    port = Column(String(10))
    user = Column(Text)
    password = Column(Text)

    def to_model(self) -> Server:
        return Server(
            name=self.name,
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password
        )

    @staticmethod
    def from_model(m: Server) -> 'ServerEntity':
        return ServerEntity(
            name=m.name,
            host=m.host,
            port=m.port,
            user=m.user,
            password=m.password
        )
