from logic.apps.servers.models.server_model import Server
from logic.libs.sqliteAlchemy import sqliteAlchemy
from sqlalchemy import Column, String

Entity = sqliteAlchemy.get_entity_class()


class ServerEntity(Entity):
    __tablename__ = 'SERVERS'

    name = Column(String, primary_key=True, nullable=False)
    host = Column(String)
    port = Column(String)
    user = Column(String)
    password = Column(String)

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
