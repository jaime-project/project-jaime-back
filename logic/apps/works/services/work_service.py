import os
import shutil
from datetime import datetime
from typing import Dict, List
from uuid import uuid4

import requests
import yaml
from logic.apps.agents.errors.agent_error import AgentError
from logic.apps.agents.models.agent_model import AgentStatus
from logic.apps.agents.services import agent_service
from logic.apps.filesystem.services import workingdir_service
from logic.apps.modules.errors.module_error import ModulesError
from logic.apps.modules.services import module_service
from logic.apps.servers.models.server_model import ServerType
from logic.apps.servers.services import server_service
from logic.apps.works.errors.work_error import WorkError
from logic.apps.works.models.work_model import Status, WorkStatus
from logic.apps.works.repositories import work_repository
from logic.apps.zip.service import zip_service
from logic.libs.exception.exception import AppException
from logic.libs.logger.logger import logger

# _WORKS_QUEUE: Dict[str, WorkStatus] = {}


def start(params: Dict[str, object]) -> str:

    _valid_params(params)

    id = _generate_id()

    work_repository.add(WorkStatus(
        id, params["name"], params["module"], params))

    return id


def exec_into_agent(work_status: WorkStatus):

    yaml_path = server_service.get_path()
    with open(yaml_path, 'r') as f:
        servers_file_bytes = f.read().encode()

    module_name = work_status.params['module']
    module_path = os.path.join(module_service.get_path(), f'{module_name}.py')
    with open(module_path, 'r') as f:
        module_file_bytes = f.read().encode()

    params_file_bytes = str(yaml.dump(work_status.params)).encode()

    url = work_status.agent.get_url() + f'/api/v1/works'
    files = {
        'servers.yaml': servers_file_bytes,
        'module.py': module_file_bytes,
        'params.yaml': params_file_bytes
    }
    payload = {
        'id': work_status.id
    }

    requests.post(url, files=files, data=payload, verify=False)
    logger().info(f'Work con id: {work_status.id} enviado')


def get(id: str) -> WorkStatus:
    return work_repository.get(id)


def delete(id: str):

    worker = get(id)
    if not worker:
        msj = f"No existe worker con id {id}"
        raise AppException(ModulesError.MODULE_NO_EXIST_ERROR, msj)

    work_repository.delete(worker)

    if worker.status == Status.RUNNING:
        agent_service.change_status(worker.agent.id, AgentStatus.READY)

    url = worker.agent.get_url() + f'/api/v1/works/{id}'
    requests.delete(url, verify=False)

    shutil.rmtree(workingdir_service.fullpath(id), ignore_errors=True)


def list_all() -> List[str]:
    return [
        work.id
        for work
        in work_repository.get_all()
    ]


def get_all_short() -> List[Dict[str, str]]:
    return [
        {
            "name": w.name,
            "status": w.status.value,
            "id": w.id,
            "agent_id": w.agent.id if w.agent else "",
            "agent_type": w.agent.type.value if w.agent else "",
            "module_name": w.module_name,
            "start_date": w.start_date.isoformat()
        }
        for w in work_repository.get_all()
    ]


def change_status(id: str, status: Status):
    work = work_repository.get(id)

    if status == Status.TERMINATED:
        work.terminated_date = datetime.now()

    if status == Status.RUNNING:
        work.running_date = datetime.now()

    work.status = status


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


def _generate_id() -> str:
    return str(uuid4()).split('-')[4]


def _valid_params(params: Dict[str, object]):

    if not 'agent' in params or not 'type' in params['agent']:
        msj = f'El tipo de agente es requerido'
        raise AppException(AgentError.AGENT_PARAM_ERROR, msj)

    agent_type = ServerType(params['agent']['type'])
    if not agent_service.get_by_type(agent_type):
        msj = f'No existen agentes de tipo {agent_type}'
        raise AppException(AgentError.AGENT_PARAM_ERROR, msj)

    module_name = params['module']
    if not module_name in module_service.list_all():
        msj = f'No existe modulo de nombre {module_name}'
        raise AppException(ModulesError.MODULE_NO_EXIST_ERROR, msj)


def _valid_work_running(id: str):

    work = get(id)

    if not work:
        msj = f'el Work con id {id} no existe'
        raise AppException(WorkError.WORK_NOT_EXIST_ERROR, msj)

    if work.status == Status.READY:
        msj = f'el Work con id {id} todabia no esta corriendo'
        raise AppException(WorkError.WORK_NOT_RUNNING_ERROR, msj)


def finish_work(id: str):

    change_status(id, Status.TERMINATED)

    agent = get(id).agent
    agent_service.change_status(agent.id, AgentStatus.READY)
