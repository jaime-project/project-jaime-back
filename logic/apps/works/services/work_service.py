import os
import shutil
from datetime import datetime
from typing import Dict, List

import requests
import yaml
from logic.apps.agents.models.agent_model import AgentStatus
from logic.apps.agents.services import agent_service
from logic.apps.filesystem.services import workingdir_service
from logic.apps.modules.errors.module_error import ModulesError
from logic.apps.works.errors.work_error import WorkError
from logic.apps.works.models.work_model import Status, Work
from logic.apps.works.repositories import work_repository
from logic.apps.zip.service import zip_service
from logic.libs.exception.exception import AppException
from logic.libs.logger.logger import logger


_PATH_AGENT_RESOURCES = 'logic/apps/agent_resources'


def add(work: Work) -> str:

    work_repository.add(work)
    return work.id


def exec_into_agent(job: Work):

    logger().info(f'Generando workingdir -> {job.id}')
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

    url = job.agent.get_url() + f'/api/v1/works/{job.id}'

    requests.post(url, verify=False)
    logger().info(f'Job enviado a agente -> {job.id}')


def get(id: str) -> Work:
    return work_repository.get(id)


def delete(id: str):

    cancel(id)
    shutil.rmtree(workingdir_service.fullpath(id), ignore_errors=True)
    work_repository.delete(id)


def cancel(id: str):

    if not work_repository.exist(id):
        msj = f"No existe worker con id {id}"
        raise AppException(ModulesError.MODULE_NO_EXIST_ERROR, msj)

    worker = get(id)

    if worker.agent in agent_service.list_all():
        url = worker.agent.get_url() + f'/api/v1/works/{id}'
        requests.delete(url, verify=False)

        agent_service.change_status(worker.agent.id, AgentStatus.READY)


def delete_by_status(status: Status):

    for id in list_by_status(status):
        delete(id)


def list_all() -> List[str]:
    return [
        work.id
        for work
        in work_repository.get_all()
    ]


def list_by_status(status: Work) -> List[str]:
    return [
        work.id
        for work
        in work_repository.get_all_by_status(status)
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
        for w in work_repository.get_all()
    ]


def change_status(id: str, status: Status):
    work = work_repository.get(id)

    if status == work.status:
        msj = f"El estado del work ya es {status.value}"
        raise AppException(WorkError.WORK_SAME_STATUS_ERROR, msj)

    if status == Status.CANCEL and work.status == Status.SUCCESS and work.status == Status.ERROR:
        msj = f"No se puede cancelar un work ya ejecutado"
        raise AppException(WorkError.WORK_INVALID_STATUS_ERROR, msj)

    if status == Status.READY and work.status == Status.RUNNING:
        msj = f"No se puede poner en READY cuando el work esta siendo ejecutado"
        raise AppException(WorkError.WORK_INVALID_STATUS_ERROR, msj)

    if status == Status.READY:
        work.running_date = None
        work.start_date = datetime.now()
        work.terminated_date = None
        work.agent = None

    if status == Status.ERROR or status == Status.SUCCESS:
        work.terminated_date = datetime.now()

    if status == Status.RUNNING:
        work.running_date = datetime.now()

    if status == Status.CANCEL:
        cancel(id)

    work.status = status
    modify(work)


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

    work = get(id)

    if not work:
        msj = f'el Work con id {id} no existe'
        raise AppException(WorkError.WORK_NOT_EXIST_ERROR, msj)

    if work.status == Status.READY:
        msj = f'el Work con id {id} todabia no esta corriendo'
        raise AppException(WorkError.WORK_NOT_RUNNING_ERROR, msj)


def finish_work(id: str, status: Status):

    change_status(id, status)

    agent = get(id).agent
    agent_service.change_status(agent.id, AgentStatus.READY)


def modify(work: Work):
    work_repository.delete(work.id)
    work_repository.add(work)


def list_types() -> str:
    return [e.value for e in Status]
