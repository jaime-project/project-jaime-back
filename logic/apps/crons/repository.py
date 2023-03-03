from typing import List

from sqlalchemy import or_

from logic.apps.crons.entity import CronEntity
from logic.apps.crons.model import CronStatus, CronJob
from logic.libs.sqliteAlchemy import sqliteAlchemy


def get_all(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[CronJob]:

    s = sqliteAlchemy.make_session()
    result = s.query(CronEntity)

    if filter:
        filter = f'%{filter}%'
        result = result.filter(or_(
            CronEntity.name.like(filter),
            CronEntity.cron_expression.like(filter),
            CronEntity.status.like(filter),
            CronEntity.creation_date.like(filter),
            CronEntity.job_module_repo.like(filter),
            CronEntity.job_module_name.like(filter),
            CronEntity.job_agent_type.like(filter),
        ))

    if order:
        result = result.order_by(order)

    if page and size:
        result = result.limit(size).offset(size * (page-1))

    result = result.all()
    s.close()

    return [r.to_model() for r in result]


def get_all_by_status(status: CronStatus) -> List[CronJob]:

    s = sqliteAlchemy.make_session()
    result = s.query(CronEntity).filter_by(status=status.value).all()
    s.close()

    return [r.to_model() for r in result]


def get(id: str) -> CronJob:

    s = sqliteAlchemy.make_session()
    result = s.query(CronEntity).get({'id': id})
    s.close()

    if result:
        return result.to_model()

    return None


def add(m: CronJob):

    s = sqliteAlchemy.make_session()

    e = CronEntity.from_model(m)
    s.add(e)

    s.commit()
    s.flush()
    s.close()


def delete(id: str):

    s = sqliteAlchemy.make_session()
    e = s.query(CronEntity).get({'id': id})
    s.delete(e)

    s.commit()
    s.flush()
    s.close()


def exist(id: str) -> bool:

    result = True

    s = sqliteAlchemy.make_session()
    if s.query(CronEntity).filter_by(id=id).count() == 0:
        result = False

    s.close()
    return result
