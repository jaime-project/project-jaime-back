from typing import Dict, List

from logic.apps.crons.errors.cron_error import CronError
from logic.apps.crons.models.cron_model import CronStatus, CronWork
from logic.apps.crons.repositories import cron_repository
from logic.apps.works.services import work_service
from logic.libs.exception.exception import AppException
from logic.libs.logger.logger import logger
from logic.apps.crons.services import cron_runner


def exec(cron: CronWork) -> str:

    work = cron.to_workStatus()
    work_service.add(work)

    logger().info(f'Cron {cron.name} -> Creando nuevo work con id {work.id}')

    return work.id


def add(cron_work: CronWork) -> str:

    if cron_repository.get(cron_work.id):
        raise AppException(CronError.CRON_ALREDY_EXIST_ERROR,
                           f'Ya existe el cron con id {id}')

    cron_repository.add(cron_work)
    return cron_work.id


def get(id: str) -> CronWork:
    return cron_repository.get(id)


def delete(id: str):
    if not cron_repository.exist(id):
        raise AppException(CronError.CRON_NOT_EXIST_ERROR,
                           f'No existe el cron con id {id}')

    cron_repository.delete(id)
    cron_runner.delete_cron_from_scheduler(id)


def delete_by_status(status: CronStatus):

    for id in list_by_status(status):
        delete(id)


def list_all() -> List[str]:
    return [
        cron.id
        for cron
        in cron_repository.get_all()
    ]


def list_by_status(status: CronWork) -> List[str]:
    return [
        cron.id
        for cron
        in cron_repository.get_all_by_status(status)
    ]


def get_all_short() -> List[Dict[str, str]]:
    return [
        {
            "name": c.name,
            "cron_expression": c.cron_expression,
            "status": c.status.value,
            "creation_date": c.creation_date.isoformat(),
            "id": c.id
        }
        for c in cron_repository.get_all()
    ]


def modify(cron: CronWork):
    cron_repository.delete(cron.id)
    cron_repository.add(cron)

    cron_runner.delete_cron_from_scheduler(cron.id)


def list_status() -> str:
    return [e.value for e in CronStatus]
