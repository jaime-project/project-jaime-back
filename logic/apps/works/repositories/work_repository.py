from typing import List

from logic.apps.works.models.work_model import WorkStatus, Status
from logic.libs.sqliteAlchemy import sqliteAlchemy

from .entities.work_entity import WorkEntity


def get_all() -> List[WorkStatus]:

    s = sqliteAlchemy.make_session()
    result = s.query(WorkEntity).all()
    s.close()

    return [r.to_model() for r in result]


def get_all_by_status(status: Status) -> List[WorkStatus]:

    s = sqliteAlchemy.make_session()
    result = s.query(WorkEntity).filter_by(status=status.value).all()
    s.close()

    return [r.to_model() for r in result]


def get(id: str) -> WorkStatus:

    s = sqliteAlchemy.make_session()
    result = s.query(WorkEntity).get({'id': id})
    s.close()

    return result.to_model()


def add(m: WorkStatus):

    s = sqliteAlchemy.make_session()

    e = WorkEntity.from_model(m)
    s.add(e)

    s.commit()
    s.flush()


def delete(id: str):

    s = sqliteAlchemy.make_session()
    e = s.query(WorkEntity).get({'id': id})
    s.delete(e)

    s.commit()
    s.flush()


def exist(id: str) -> bool:

    s = sqliteAlchemy.make_session()
    if s.query(WorkEntity).filter_by(id=id).count() == 0:
        return False

    return True
