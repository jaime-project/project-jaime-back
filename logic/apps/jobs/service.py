import shutil
from datetime import datetime
from typing import Dict, List

import requests
import yaml

from logic.apps.agents import service as agent_service
from logic.apps.agents.model import AgentStatus
from logic.apps.filesystem import workingdir_service
from logic.apps.jobs import repository as job_repository
from logic.apps.jobs.error import JobError
from logic.apps.jobs.model import Job, Status
from logic.apps.modules.error import ModulesError
from logic.apps.repos import service as repo_service
from logic.apps.zip import service as zip_service
from logic.libs.exception.exception import AppException
from logic.libs.logger import logger


def add(job: Job) -> str:

    job_repository.add(job)
    return job.id


def exec_into_agent(job: Job):

    logger.log.info(f'Making workingdir -> {job.id}')
    workingdir_service.create_by_id(job.id)

    workingdir_path = workingdir_service.fullpath(job.id)

    shutil.copy(
        f'{repo_service.get_path()}/{job.module_repo}/{job.module_name}.py',
        f'{workingdir_path}/module.py'
    )

    with open(f'{workingdir_path}/params.yaml', 'w') as f:
        f.write(yaml.dump(job.params))

    url = job.agent.get_url() + f'/api/v1/jobs/{job.id}'

    requests.post(url, verify=False)
    logger.log.info(f'Job sended to agent -> {job.id}')


def get(id: str) -> Job:
    return job_repository.get(id)


def delete(id: str):

    cancel(id)
    shutil.rmtree(workingdir_service.fullpath(id), ignore_errors=True)
    job_repository.delete(id)


def cancel(id: str):

    if not job_repository.exist(id):
        msj = f"id job not found -> {id}"
        raise AppException(ModulesError.MODULE_NO_EXIST_ERROR, msj)

    job = get(id)

    if job.agent in agent_service.list_all():
        url = job.agent.get_url() + f'/api/v1/jobs/{id}'
        requests.delete(url, verify=False)

        agent_service.change_status(job.agent.id, AgentStatus.READY)


def delete_by_status(status: Status):

    for id in list_by_status(status):
        delete(id)


def list_all() -> List[str]:
    return [
        job.id
        for job
        in job_repository.get_all()
    ]


def list_by_status(status: Status) -> List[str]:
    return [
        job.id
        for job
        in job_repository.get_all_by_status(status)
    ]


def get_all_short(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[Dict[str, str]]:
    return [
        {
            "name": w.name,
            "status": w.status.value,
            "id": w.id,
            "agent_id": w.agent.id if w.agent else "",
            "agent_type": w.agent.type if w.agent else "",
            "module_name": w.module_name,
            "start_date": w.start_date.isoformat() if w.start_date else ""
        }
        for w in job_repository.get_all(size, page, filter, order)
    ]


def change_status(id: str, status: Status):
    job = job_repository.get(id)

    if status == Status.READY and job.status == Status.RUNNING and job.agent and agent_service.get(job.agent.id):
        msj = f"You can't change status to READY when job still running"
        raise AppException(JobError.WORK_INVALID_STATUS_ERROR, msj)

    if status == Status.READY:
        job.running_date = None
        job.start_date = datetime.now()
        job.terminated_date = None
        job.agent = None

    if status == Status.ERROR or status == Status.SUCCESS:
        job.terminated_date = datetime.now()

    if status == Status.RUNNING:
        job.running_date = datetime.now()

    if status == Status.CANCEL:
        cancel(id)

    job.status = status
    modify(job)


def get_logs(id: str) -> str:

    _valid_work_running(id)

    with open(workingdir_service.getLogsPath(id), 'r') as f:
        return f.read()


def download_workspace(id) -> bytes:

    _valid_work_running(id)

    zip_result_path = workingdir_service.fullpath(id) + '.zip'
    path = workingdir_service.fullpath(id)

    zip_service.create(zip_result_path, path)

    final_zip_path = workingdir_service.fullpath(id) + f'/{id}.zip'
    shutil.move(zip_result_path, final_zip_path)

    return open(final_zip_path, 'rb').read()


def _valid_work_running(id: str):

    job = get(id)

    if not job:
        msj = f'Job with id {id} not found'
        raise AppException(JobError.WORK_NOT_EXIST_ERROR, msj)

    if job.status == Status.READY:
        msj = f'Job with id {id} yet not running'
        raise AppException(JobError.WORK_NOT_RUNNING_ERROR, msj)


def finish_work(id: str, status: Status):

    change_status(id, status)

    agent = get(id).agent
    agent_service.change_status(agent.id, AgentStatus.READY)


def modify(job: Job):
    job_repository.delete(job.id)
    job_repository.add(job)


def list_types() -> str:
    return [e.value for e in Status]
