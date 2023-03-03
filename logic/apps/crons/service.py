from typing import Dict, List

from logic.apps.crons import repository, runner
from logic.apps.crons.error import CronError
from logic.apps.crons.model import CronStatus, CronJob
from logic.apps.jobs import service as job_service
from logic.libs.exception.exception import AppException
from logic.libs.logger import logger


def exec(cron: CronJob) -> str:

    job = cron.to_workStatus()
    job_service.add(job)

    logger.log.info(f'Cron {cron.name} -> Making new job with id {job.id}')

    return job.id


def add(cron_work: CronJob) -> str:

    if repository.get(cron_work.id):
        raise AppException(CronError.CRON_ALREDY_EXIST_ERROR,
                           f'There are a cron with id {id}')

    repository.add(cron_work)
    return cron_work.id


def get(id: str) -> CronJob:
    return repository.get(id)


def get_all(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[CronJob]:
    return repository.get_all(size, page, filter, order)


def delete(id: str):
    if not repository.exist(id):
        raise AppException(CronError.CRON_NOT_EXIST_ERROR,
                           f'There are no cron with id {id}')

    repository.delete(id)
    runner.delete_cron_from_scheduler(id)


def delete_by_status(status: CronStatus):

    for id in list_by_status(status):
        delete(id)


def list_all() -> List[str]:
    return [
        cron.id
        for cron
        in repository.get_all()
    ]


def list_by_status(status: CronJob) -> List[str]:
    return [
        cron.id
        for cron
        in repository.get_all_by_status(status)
    ]


def get_all_short(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[Dict[str, str]]:
    return [
        {
            "name": c.name,
            "cron_expression": c.cron_expression,
            "status": c.status.value,
            "creation_date": c.creation_date.isoformat(),
            "id": c.id
        }
        for c in repository.get_all(size, page, filter, order)
    ]


def modify(cron: CronJob):
    repository.delete(cron.id)
    repository.add(cron)

    runner.delete_cron_from_scheduler(cron.id)


def list_status() -> str:
    return [e.value for e in CronStatus]
