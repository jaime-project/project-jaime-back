from typing import Dict, List

from logic.apps.hooks import repository
from logic.apps.hooks.error import HookError
from logic.apps.hooks.model import HookJob, HookStatus
from logic.apps.jobs import service as job_service
from logic.libs.exception.exception import AppException
from logic.libs.logger import logger


def exec(hook: HookJob, params: dict[str, object] = {}) -> str:
    if hook.status == HookStatus.DESACTIVE:
        raise AppException(
            HookError.HOOK_NOT_ACTIVE_ERROR,
            f"Hook with name {hook.name} is {HookStatus.DESACTIVE}",
        )

    job = hook.to_job()
    job.params.update(params)

    job_service.add(job)

    logger.log.info(f"hook {hook.name} -> Making new job with id {job.id}")

    return job.id


def add(hook: HookJob) -> str:
    if repository.get(hook.id):
        raise AppException(
            HookError.HOOK_ALREDY_EXIST_ERROR, f"There are a hook with id {id}"
        )

    repository.add(hook)
    return hook.id


def get(id: str) -> HookJob:
    return repository.get(id)


def get_all(
    size: int = 10, page: int = 1, filter: str = None, order: str = None
) -> List[HookJob]:
    return repository.get_all(size, page, filter, order)


def delete(id: str):
    if not repository.exist(id):
        raise AppException(
            HookError.HOOK_NOT_EXIST_ERROR, f"There are no hook with id {id}"
        )

    repository.delete(id)


def delete_by_status(status: HookStatus):
    for id in list_by_status(status):
        delete(id)


def list_all() -> List[str]:
    return [hook.id for hook in repository.get_all()]


def list_by_status(status: HookJob) -> List[str]:
    return [hook.id for hook in repository.get_all_by_status(status)]


def get_all_short(
    size: int = 10, page: int = 1, filter: str = None, order: str = None
) -> List[Dict[str, str]]:
    return [
        {
            "name": c.name,
            "status": c.status.value,
            "creation_date": c.creation_date.isoformat(),
            "id": c.id,
        }
        for c in repository.get_all(size, page, filter, order)
    ]


def modify(hook: HookJob):
    repository.delete(hook.id)
    repository.add(hook)


def list_status() -> str:
    return [e.value for e in HookStatus]


def desactivate_cron(id: str):
    cron = get(id)
    cron.status = HookStatus.DESACTIVE

    modify(cron)


def activate_cron(id: str):
    cron = get(id)
    cron.status = HookStatus.ACTIVE

    modify(cron)
