import urllib.request
from typing import Dict, List

import requests
from logic.apps.agents.errors.agent_error import AgentError
from logic.apps.agents.models.agent_model import Agent
from logic.apps.works.services import work_service
from logic.libs.exception.exception import AppException
from logic.libs.logger.logger import logger

_AGENTS_ONLINE: Dict[str, Agent] = {}


def add(node: Agent):

    global _AGENTS_ONLINE

    if node in _AGENTS_ONLINE.values():
        msj = f'Ya existe un agente con el id {node.id}'
        raise AppException(AgentError.AGENT_ALREADY_EXIST_ERROR, msj)

    id = node.id
    _AGENTS_ONLINE[id] = node


def delete(id: str):
    global _AGENTS_ONLINE

    _AGENTS_ONLINE = {
        (k, v)
        for k, v in _AGENTS_ONLINE.items()
        if k != id
    }


def get(id: str) -> Agent:
    global _AGENTS_ONLINE

    if id not in _AGENTS_ONLINE.keys():
        msj = f'No existe nodo con el id {id}'
        raise AppException(AgentError.AGENT_NOT_EXIST_ERROR)

    return _AGENTS_ONLINE[id]


def is_alive(id: str) -> bool:

    node = get(id)

    try:
        url_alive = node.get_url()
        return requests.get(url_alive).getcode() == 200

    except Exception as e:
        logger().exception(e)
        return False


def get_by_type(type: str) -> List[Agent]:
    global _AGENTS_ONLINE

    return [
        n
        for n in _AGENTS_ONLINE.values()
        if n.type == type
    ]


def list_all() -> List[Agent]:
    return _AGENTS_ONLINE.values()


def get_logs(id: str) -> str:

    agent = get(id)

    url = agent.get_url() + f'/api/v1/works/{id}/logs'
    result = requests.get(url).content
    return result.decode() if result else ""


def get_available_agent_by_type(type: str) -> Agent:

    agents = get_by_type(type)
    if not agents:
        msj = f'No existe agente con el tipo {type}'
        raise AppException(AgentError.AGENT_NOT_EXIST_ERROR)

    agents_working = [
        work_service.get(id_w).agent
        for id_w in work_service.list_all()
    ]

    for a in agents:
        if a not in agents_working:
            return a

    return None
