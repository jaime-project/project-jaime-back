from logic.apps.servers.models.server_model import Server, ServerType
from logic.libs.sqliteAlchemy import sqliteAlchemy
from sqlalchemy import Column, String

Entity = sqliteAlchemy.get_entity_class()


class ServerEntity(Entity):
    __tablename__ = 'SERVERS'

    name = Column(String, primary_key=True, nullable=False)
    url = Column(String)
    token = Column(String)
    type = Column(String)
    version = Column(String)

    def to_model(self) -> Server:
        return Server(
            name=self.name,
            url=self.url,
            token=self.token,
            type=ServerType(self.type),
            version=self.version
        )

    @staticmethod
    def from_model(m: Server) -> 'ServerEntity':
        return ServerEntity(
            name=m.name,
            url=m.url,
            token=m.token,
            type=m.type.value,
            version=m.version
        )
