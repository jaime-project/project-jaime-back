
from typing import Dict

from logic.libs.sqliteAlchemy import sqliteAlchemy
from sqlalchemy import Column, String

Entity = sqliteAlchemy.get_entity_class()


class ConfigEntity(Entity):
    __tablename__ = 'CONFIGS'

    key = Column(String(255), primary_key=True, nullable=False)
    value = Column(String(255))

    def to_model(self) -> Dict[str, str]:
        return {
            self.key: self.value
        }

    @staticmethod
    def from_model(k: str, v: str) -> 'ConfigEntity':
        return ConfigEntity(key=k, value=v)
