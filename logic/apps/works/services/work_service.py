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
from logic.apps.clusters.models.cluster_model import ClusterType
from logic.apps.clusters.services import cluster_service
from logic.apps.filesystem.services import workingdir_service
from logic.apps.modules.errors.module_error import ModulesError
from logic.apps.modules.services import module_service
from logic.apps.servers.services import server_service
from logic.apps.works.errors.work_error import WorkError
from logic.apps.works.models.work_model import Status, WorkStatus
from logic.apps.works.repositories import work_repository
from logic.apps.zip.service import zip_service
from logic.libs.exception.exception import AppException
from logic.libs.logger.logger import logger


def start(params: Dict[str, object]) -> str:

    _valid_params(params)

    id = _generate_id()

    work_repository.add(WorkStatus(id, params))

    return id


def exec_into_agent(work_status: WorkStatus):

    module_name = work_status.params['module']['name']
    module_repo = work_status.params['module']['repo']
    module_path = os.path.join(
        module_service.get_path(), f'{module_repo}/{module_name}.py')
    with open(module_path, 'r') as f:
        module_file_bytes = f.read().encode()

    clusters_dict = [
        c.__dict__()
        for c in cluster_service.get_all()
    ]
    clusters_file_bytes = str(yaml.dump(clusters_dict)).encode()

    servers_dict = [
        s.__dict__()
        for s in server_service.get_all()
    ]
    servers_file_bytes = str(yaml.dump(servers_dict)).encode()

    params_file_bytes = str(yaml.dump(work_status.params)).encode()

    url = work_status.agent.get_url() + f'/api/v1/works'
    files = {
        'clusters.yaml': clusters_file_bytes,
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

    cancel(id)
    shutil.rmtree(workingdir_service.fullpath(id), ignore_errors=True)
    work_repository.delete(id)


def cancel(id: str):

    if not work_repository.exist(id):
        msj = f"No existe worker con id {id}"
        raise AppException(ModulesError.MODULE_NO_EXIST_ERROR, msj)

    worker = get(id)

    if worker.agent:
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


def list_by_status(status: WorkStatus) -> List[str]:
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
            "agent_type": w.agent.type.value if w.agent else "",
            "module_name": w.module_name,
            "start_date": w.start_date.isoformat()
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


def _generate_id() -> str:
    return str(uuid4()).split('-')[4]


def _valid_params(params: Dict[str, object]):

    if not 'agent' in params or not 'type' in params['agent']:
        msj = f'El tipo de agente es requerido'
        raise AppException(AgentError.AGENT_PARAM_ERROR, msj)

    agent_type = ClusterType(params['agent']['type'])
    if not agent_service.get_by_type(agent_type):
        msj = f'No existen agentes activos de tipo {agent_type}'
        raise AppException(AgentError.AGENT_PARAM_ERROR, msj)

    if not 'module' in params or not 'repo' in params['module'] or not 'name' in params['module'] or not params['module']['name'] in module_service.list_all(params['module']['repo']):
        name = params['module']['name']
        msj = f'No existe modulo de nombre {name}'
        raise AppException(ModulesError.MODULE_NO_EXIST_ERROR, msj)


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


def modify(work: WorkStatus):
    work_repository.delete(work.id)
    work_repository.add(work)


def list_types() -> str:
    return [e.value for e in Status]
