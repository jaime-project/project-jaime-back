from typing import Dict, List

import requests
from logic.apps.agents.errors.agent_error import AgentError
from logic.apps.agents.models.agent_model import Agent
from logic.apps.works.models.work_model import Status
from logic.apps.works.services import work_service
from logic.libs.exception.exception import AppException
from logic.libs.logger.logger import logger

_AGENTS_ONLINE: Dict[str, Agent] = {}


def add(agent: Agent):

    global _AGENTS_ONLINE

    if agent in list_all():
        msj = f'Ya existe un agente con el id {agent.id}'
        raise AppException(AgentError.AGENT_ALREADY_EXIST_ERROR, msj)

    id = agent.id
    _AGENTS_ONLINE[id] = agent

    logger().info(f'Nuevo agente conectado -> id: {id}')


def delete(id: str):

    global _AGENTS_ONLINE

    new_dict = {}
    for k, v in _AGENTS_ONLINE.items():
        if k != id:
            new_dict[k] = v

    _AGENTS_ONLINE = new_dict


def disconnec_agent(id):

    agent = get(id)
    url = agent.get_url() + '/api/v1/jaime/'
    requests.delete(url)


def get(id: str) -> Agent:
    global _AGENTS_ONLINE

    if id not in _AGENTS_ONLINE.keys():
        msj = f'No existe nodo con el id {id}'
        raise AppException(AgentError.AGENT_NOT_EXIST_ERROR)

    return _AGENTS_ONLINE[id]


def is_alive(id: str) -> bool:

    agent = get(id)

    try:
        request = requests.get(f'{agent.get_url()}/alive', verify=False)

        status_code_ok = request.status_code == 200
        id_ok = request.json().get('id') == id

        return status_code_ok and id_ok

    except Exception as e:
        return False


def get_by_type(type: str) -> List[Agent]:
    global _AGENTS_ONLINE

    return [
        n
        for _, n in _AGENTS_ONLINE.items()
        if n.type.lower() == type.lower()
    ]


def list_all() -> List[Agent]:
    global _AGENTS_ONLINE
    if not _AGENTS_ONLINE:
        return []

    return _AGENTS_ONLINE.values()


def get_available_agent_by_type(type: str) -> Agent:

    agents = get_by_type(type)
    if not agents:
        msj = f'No existe agente con el tipo {type}'
        raise AppException(AgentError.AGENT_NOT_EXIST_ERROR)

    agents_working = [
        work_service.get(id_w).agent
        for id_w in work_service.list_all()
        if work_service.get(id_w).status == Status.RUNNING
    ]

    for a in agents:
        if a not in agents_working:
            return a

    return None


def get_all_short() -> List[Dict[str, str]]:
    global _AGENTS_ONLINE

    return [
        {
            "id": n.id,
            "host": n.host,
            "port": n.port,
            "type": n.type.value
        }
        for _, n in _AGENTS_ONLINE.items()
    ]
