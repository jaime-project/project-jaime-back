import os
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
from logic.apps.zip import service as zip_service
from logic.libs.exception.exception import AppException
from logic.libs.logger import logger

_PATH_AGENT_RESOURCES = 'logic/apps/agent_resources'


def add(job: Job) -> str:

    job_repository.add(job)
    return job.id


def exec_into_agent(job: Job):

    logger.log.info(f'Generando workingdir -> {job.id}')
    workingdir_service.create_by_id(job.id)

    workingdir_path = workingdir_service.fullpath(job.id)

    runner_script = 'runner.pyc' if os.path.exists(
        f'{_PATH_AGENT_RESOURCES}/runner.pyc') else 'runner.py'
    shutil.copy(f'{_PATH_AGENT_RESOURCES}/{runner_script}', workingdir_path)

    tools_script = 'tools.pyc' if os.path.exists(
        f'{_PATH_AGENT_RESOURCES}/tools.pyc') else 'tools.py'
    shutil.copy(f'{_PATH_AGENT_RESOURCES}/{tools_script}', workingdir_path)

    shutil.copy(job.get_module_file_path(), f'{workingdir_path}/module.py')

    with open(f'{workingdir_path}/params.yaml', 'w') as f:
        f.write(yaml.dump(job.params))

    url = job.agent.get_url() + f'/api/v1/jobs/{job.id}'

    requests.post(url, verify=False)
    logger.log.info(f'Job enviado a agente -> {job.id}')


def get(id: str) -> Job:
    return job_repository.get(id)


def delete(id: str):

    cancel(id)
    shutil.rmtree(workingdir_service.fullpath(id), ignore_errors=True)
    job_repository.delete(id)


def cancel(id: str):

    if not job_repository.exist(id):
        msj = f"No existe worker con id {id}"
        raise AppException(ModulesError.MODULE_NO_EXIST_ERROR, msj)

    worker = get(id)

    if worker.agent in agent_service.list_all():
        url = worker.agent.get_url() + f'/api/v1/jobs/{id}'
        requests.delete(url, verify=False)

        agent_service.change_status(worker.agent.id, AgentStatus.READY)


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


def get_all_short() -> List[Dict[str, str]]:
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
        for w in job_repository.get_all()
    ]


def change_status(id: str, status: Status):
    job = job_repository.get(id)

    if status == job.status:
        msj = f"El estado del job ya es {status.value}"
        raise AppException(JobError.WORK_SAME_STATUS_ERROR, msj)

    if status == Status.READY and job.status == Status.RUNNING:
        msj = f"No se puede poner en READY cuando el job esta siendo ejecutado"
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
        msj = f'el Job con id {id} no existe'
        raise AppException(JobError.WORK_NOT_EXIST_ERROR, msj)

    if job.status == Status.READY:
        msj = f'el Job con id {id} todabia no esta corriendo'
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
