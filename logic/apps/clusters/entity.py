from sqlalchemy import Column, String, Text

from logic.apps.clusters.model import Cluster
from logic.libs.sqliteAlchemy import sqliteAlchemy

Entity = sqliteAlchemy.get_entity_class()


class ClusterEntity(Entity):
    __tablename__ = 'CLUSTERS'

    name = Column(String(255), primary_key=True, nullable=False)
    url = Column(Text)
    token = Column(Text)
    type = Column(String(60))
    version = Column(String(255))

    def to_model(self) -> Cluster:
        return Cluster(
            name=self.name,
            url=self.url,
            token=self.token,
            type=self.type,
            version=self.version
        )

    @staticmethod
    def from_model(m: Cluster) -> 'ClusterEntity':
        return ClusterEntity(
            name=m.name,
            url=m.url,
            token=m.token,
            type=m.type,
            version=m.version
        )
