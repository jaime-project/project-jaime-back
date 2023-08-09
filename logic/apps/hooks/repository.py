from typing import List

from sqlalchemy import or_

from logic.apps.hooks.entity import HookEntity
from logic.apps.hooks.model import HookJob, HookStatus
from logic.libs.sqliteAlchemy import sqliteAlchemy


def get_all(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[HookJob]:

    s = sqliteAlchemy.make_session()
    result = s.query(HookEntity)

    if filter:
        filter = f'%{filter}%'
        result = result.filter(or_(
            HookEntity.name.like(filter),
            HookEntity.status.like(filter),
            HookEntity.creation_date.like(filter),
            HookEntity.job_module_repo.like(filter),
            HookEntity.job_module_name.like(filter),
            HookEntity.job_agent_type.like(filter),
        ))

    if order:
        result = result.order_by(order)

    if page and size:
        result = result.limit(size).offset(size * (page-1))

    result = result.all()
    s.close()

    return [r.to_model() for r in result]


def get_all_by_status(status: HookStatus) -> List[HookJob]:

    s = sqliteAlchemy.make_session()
    result = s.query(HookEntity).filter_by(status=status.value).all()
    s.close()

    return [r.to_model() for r in result]


def get(id: str) -> HookJob:

    s = sqliteAlchemy.make_session()
    result = s.query(HookEntity).get({'id': id})
    s.close()

    if result:
        return result.to_model()

    return None


def add(m: HookJob):

    s = sqliteAlchemy.make_session()

    e = HookEntity.from_model(m)
    s.add(e)

    s.commit()
    s.flush()
    s.close()


def delete(id: str):

    s = sqliteAlchemy.make_session()
    e = s.query(HookEntity).get({'id': id})
    s.delete(e)

    s.commit()
    s.flush()
    s.close()


def exist(id: str) -> bool:

    result = True

    s = sqliteAlchemy.make_session()
    if s.query(HookEntity).filter_by(id=id).count() == 0:
        result = False

    s.close()
    return result
