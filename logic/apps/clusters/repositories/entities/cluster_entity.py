from logic.apps.clusters.models.cluster_model import Cluster, ClusterType
from logic.libs.sqliteAlchemy import sqliteAlchemy
from sqlalchemy import Column, String

Entity = sqliteAlchemy.get_entity_class()


class ClusterEntity(Entity):
    __tablename__ = 'CLUSTERS'

    name = Column(String, primary_key=True, nullable=False)
    url = Column(String)
    token = Column(String)
    type = Column(String)
    version = Column(String)

    def to_model(self) -> Cluster:
        return Cluster(
            name=self.name,
            url=self.url,
            token=self.token,
            type=ClusterType(self.type),
            version=self.version
        )

    @staticmethod
    def from_model(m: Cluster) -> 'ClusterEntity':
        return ClusterEntity(
            name=m.name,
            url=m.url,
            token=m.token,
            type=m.type.value,
            version=m.version
        )
