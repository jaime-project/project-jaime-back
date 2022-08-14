from typing import List

from logic.apps.crons.models.cron_model import CronStatus, CronWork
from logic.libs.sqliteAlchemy import sqliteAlchemy

from .entities.cron_entity import CronEntity


def get_all() -> List[CronWork]:

    s = sqliteAlchemy.make_session()
    result = s.query(CronEntity).all()
    s.close()

    return [r.to_model() for r in result]


def get_all_by_status(status: CronStatus) -> List[CronWork]:

    s = sqliteAlchemy.make_session()
    result = s.query(CronEntity).filter_by(status=status.value).all()
    s.close()

    return [r.to_model() for r in result]


def get(id: str) -> CronWork:

    s = sqliteAlchemy.make_session()
    result = s.query(CronEntity).get({'id': id})
    s.close()

    if result:
        return result.to_model()

    return None


def add(m: CronWork):

    s = sqliteAlchemy.make_session()

    e = CronEntity.from_model(m)
    s.add(e)

    s.commit()
    s.flush()


def delete(id: str):

    s = sqliteAlchemy.make_session()
    e = s.query(CronEntity).get({'id': id})
    s.delete(e)

    s.commit()
    s.flush()


def exist(id: str) -> bool:

    result = True

    s = sqliteAlchemy.make_session()
    if s.query(CronEntity).filter_by(id=id).count() == 0:
        result = False

    s.close()
    return result
