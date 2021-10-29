from datetime import datetime
from typing import Dict, List
from uuid import uuid4

from logic.apps.agents.errors.agent_error import AgentError
from logic.apps.agents.models.agent_model import Agent
from logic.apps.agents.services import agent_service
from logic.apps.filesystem.services import workingdir_service
from logic.apps.modules.errors.module_error import ModulesError
from logic.apps.works.errors.work_error import WorkError
from logic.apps.works.models.work_model import Status, WorkStatus
from logic.libs.exception.exception import AppException

_WORKS_QUEUE: Dict[str, WorkStatus] = {}


def start(params: Dict[str, object]) -> str:

    if not 'agent' in params or not 'type' in params['agent']:
        msj = f'El tipo de agente es requerido'
        raise AppException(AgentError.AGENT_PARAM_ERROR, msj)

    agent_type = params['agent']['type']
    if not agent_service.get_by_type(agent_type):
        msj = f'No se encontro agentes de tipo {agent_type}'
        raise AppException(AgentError.AGENT_PARAM_ERROR, msj)

    id = _generate_id()

    global _WORKS_QUEUE
    _WORKS_QUEUE[id] = WorkStatus(id)

    return id


def get(id: str) -> WorkStatus:
    global _WORKS_QUEUE
    return _WORKS_QUEUE.get(id, None)


def delete(id: str):
    global _WORKS_QUEUE

    worker = get(id)
    if not worker:
        msj = f"No existe worker con id {id}"
        raise AppException(ModulesError.MODULE_NO_EXIST_ERROR, msj)

    _WORKS_QUEUE = {
        k: v
        for k, v in _WORKS_QUEUE.items()
        if k != id
    }


def list_all() -> List[str]:
    global _WORKS_QUEUE
    return _WORKS_QUEUE.keys()


def change_status(id: str, status: Status):
    global _WORKS_QUEUE
    work = _WORKS_QUEUE[id]

    if status == Status.TERMINATED:
        work.terminated_date = datetime.now()

    if status == Status.RUNNING:
        work.running_date = datetime.now()

    work.status = status


def _generate_id() -> str:
    return str(uuid4()).split('-')[4]


def get_logs(id: str) -> str:

    global _WORKS_QUEUE
    if not id in _WORKS_QUEUE:
        msj = f'el Work con id {id} todabia no esta corriendo'
        raise AppException(WorkError.WORK_NOT_RUNNING_ERROR, msj)

    return agent_service.get_logs(id)
