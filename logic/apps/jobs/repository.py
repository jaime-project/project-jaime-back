from typing import List

from sqlalchemy import or_, and_

from logic.apps.jobs.entity import JobEntity
from logic.apps.jobs.model import Job, Status
from logic.libs.sqliteAlchemy import sqliteAlchemy


def get_all(size: int = 10, page: int = 1, filter: str = None, order: str = None, status: Status = None) -> List[Job]:

    s = sqliteAlchemy.make_session()
    result = s.query(JobEntity)

    if status:
        result = result.filter(JobEntity.status == status.value)

    if filter:
        filter = f'%{filter}%'
        result = result.filter(or_(
            JobEntity.id.like(filter),
            JobEntity.name.like(filter),
            JobEntity.module_name.like(filter),
            JobEntity.module_repo.like(filter),
            JobEntity.params.like(filter),
            JobEntity.agent.like(filter),
            JobEntity.agent_type.like(filter),
        ))

    if order:
        result = result.order_by(order)

    if page and size:
        result = result.limit(size).offset(size * (page-1))

    result = result.all()
    s.close()

    return [r.to_model() for r in result]


def get_all_by_status(status: Status) -> List[Job]:

    s = sqliteAlchemy.make_session()
    result = s.query(JobEntity).filter_by(status=status.value).all()
    s.close()

    return [r.to_model() for r in result]


def get(id: str) -> Job:

    s = sqliteAlchemy.make_session()
    result = s.query(JobEntity).get({'id': id})
    s.close()

    if result:
        return result.to_model()

    return None


def add(m: Job):

    s = sqliteAlchemy.make_session()

    e = JobEntity.from_model(m)
    s.add(e)

    s.commit()
    s.flush()


def delete(id: str):

    s = sqliteAlchemy.make_session()
    e = s.query(JobEntity).get({'id': id})
    s.delete(e)

    s.commit()
    s.flush()


def exist(id: str) -> bool:

    result = True

    s = sqliteAlchemy.make_session()
    if s.query(JobEntity).filter_by(id=id).count() == 0:
        result = False

    s.close()
    return result
