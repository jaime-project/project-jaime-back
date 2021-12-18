import os
from datetime import datetime
from typing import Dict, List
from uuid import uuid4

import requests
import yaml
from logic.apps.agents.errors.agent_error import AgentError
from logic.apps.agents.services import agent_service
from logic.apps.modules.errors.module_error import ModulesError
from logic.apps.modules.services import module_service
from logic.apps.servers.models.server_model import ServerType
from logic.apps.servers.services import server_service
from logic.apps.works.errors.work_error import WorkError
from logic.apps.works.models.work_model import Status, WorkStatus
from logic.libs.exception.exception import AppException

_WORKS_QUEUE: Dict[str, WorkStatus] = {}


def start(params: Dict[str, object]) -> str:

    _valid_params(params)

    id = _generate_id()

    global _WORKS_QUEUE
    _WORKS_QUEUE[id] = WorkStatus(id, params["name"], params["module"], params)

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


def get(id: str) -> WorkStatus:
    global _WORKS_QUEUE
    return _WORKS_QUEUE.get(id, None)


def delete(id: str):
    global _WORKS_QUEUE

    worker = get(id)
    if not worker:
        msj = f"No existe worker con id {id}"
        raise AppException(ModulesError.MODULE_NO_EXIST_ERROR, msj)
    
    _WORKS_QUEUE.pop(id)


def list_all() -> List[str]:
    global _WORKS_QUEUE
    return _WORKS_QUEUE.keys()


def get_all_short() -> List[Dict[str, str]]:
    global _WORKS_QUEUE
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
        for _, w in _WORKS_QUEUE.items()
    ]


def change_status(id: str, status: Status):
    global _WORKS_QUEUE
    work = _WORKS_QUEUE[id]

    if status == Status.TERMINATED:
        work.terminated_date = datetime.now()

    if status == Status.RUNNING:
        work.running_date = datetime.now()

    work.status = status


def get_logs(id: str) -> str:

    _valid_work_running(id)

    agent = get(id).agent

    url = agent.get_url() + f'/api/v1/works/{id}/logs'
    result = requests.get(url, verify=False).content
    return result.decode() if result else ""


def download_workspace(id):

    _valid_work_running(id)

    agent = get(id).agent
    url = agent.get_url() + f'/api/v1/works/{id}/workspace'
    response = requests.get(url, verify=False)
    return response.content


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
