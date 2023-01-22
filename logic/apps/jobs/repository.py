from typing import List

from logic.apps.jobs.entity import JobEntity
from logic.apps.jobs.model import Job, Status
from logic.libs.sqliteAlchemy import sqliteAlchemy


def get_all() -> List[Job]:

    s = sqliteAlchemy.make_session()
    result = s.query(JobEntity).all()
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
