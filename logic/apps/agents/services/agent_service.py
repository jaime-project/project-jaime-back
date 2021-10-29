import urllib.request
from typing import Dict, List

from logic.apps.agents.errors.agent_error import AgentError
from logic.apps.agents.models.agent_model import Agent
from logic.libs.exception.exception import AppException
from logic.libs.logger.logger import logger

_AGENTS_ONLINE: Dict[str, Agent] = {}


def add(node: Agent):

    global _AGENTS_ONLINE

    if node in _AGENTS_ONLINE.values():
        msj = f'Ya existe un nodo con el id {node.id}'
        raise AppException(AgentError.NODE_ALREADY_EXIST_ERROR, msj)

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
        raise AppException(AgentError.NODE_NOT_EXIST_ERROR)

    return _AGENTS_ONLINE[id]


def is_alive(id: str) -> bool:

    node = get(id)

    try:
        url_alive = node.get_url()
        return urllib.request.urlopen(url_alive).getcode() == 200

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
