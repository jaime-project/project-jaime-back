from sqlalchemy import Column, String, Text

from logic.apps.libraries.model import Library
from logic.libs.sqliteAlchemy import sqliteAlchemy

Entity = sqliteAlchemy.get_entity_class()


class LibraryEntity(Entity):
    __tablename__ = 'LIBRARIES'

    name = Column(String(60), primary_key=True, nullable=False)
    description = Column(Text)
    repo = Column(String(255))
    path = Column(String(255))
    branch = Column(String(60))
    user = Column(Text)
    password = Column(Text)

    def to_model(self) -> Library:
        return Library(
            name=self.name,
            description=self.description,
            repo=self.repo,
            path=self.path,
            branch=self.branch,
            user=self.user,
            password=self.password
        )

    @staticmethod
    def from_model(m: Library) -> 'LibraryEntity':
        return LibraryEntity(
            name=m.name,
            description=m.description,
            repo=m.repo,
            path=m.path,
            branch=m.branch,
            user=m.user,
            password=m.password
        )
