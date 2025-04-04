from typing import Dict, List

import requests

from logic.apps.agents.error import AgentError
from logic.apps.agents.model import Agent, AgentStatus
from logic.apps.configs import service
from logic.libs.exception.exception import AppException
from logic.libs.logger import logger

_AGENTS_ONLINE: Dict[str, Agent] = {}

_AGENTS_TYPES: List[str] = []


def add(agent: Agent):

    global _AGENTS_ONLINE

    if agent in list_all():
        logger.log.warning(f'There is already an agent with the id {agent.id}')

    _AGENTS_ONLINE[agent.id] = agent

    add_agent_type(agent.type)

    service.update_requirements(service.get_requirements())
    logger.log.info(f'New agent connected -> id: {str(agent.id)}')
    print(_AGENTS_ONLINE)


def delete(id: str):

    try:
        disconnec_agent(id)
    except Exception as e:
        logger.log.error(e)

    agent_type = get(id).type
    delete_agent_type(agent_type)

    global _AGENTS_ONLINE
    _AGENTS_ONLINE.pop(id)


def disconnec_agent(id):

    agent = get(id)
    url = agent.get_url() + '/api/v1/jaime/'
    requests.delete(url, timeout=1)


def get(id: str) -> Agent:
    global _AGENTS_ONLINE
    return _AGENTS_ONLINE.get(id, None)


def is_alive(id: str) -> bool:

    agent = get(id)

    try:
        request = requests.get(
            f'{agent.get_url()}/alive', verify=False, timeout=2)

        status_code_ok = request.status_code == 200
        id_ok = request.json().get('id') == id

        return status_code_ok and id_ok

    except Exception as e:
        logger.log.warning(e)
        return False


def get_by_type(type: str) -> List[Agent]:
    global _AGENTS_ONLINE
    print(_AGENTS_ONLINE)
    
    return [
        n
        for _, n in _AGENTS_ONLINE.items()
        if n.type == type.upper().lstrip()
    ]


def list_all() -> List[Agent]:
    global _AGENTS_ONLINE
    if not _AGENTS_ONLINE:
        return []

    return list(_AGENTS_ONLINE.values())


def get_available_agent_by_type(type: str) -> Agent:

    agents = get_by_type(type)
    if not agents:
        msj = f'There are no available {type} agent'
        raise AppException(AgentError.AGENT_NOT_EXIST_ERROR, msj)

    for a in agents:
        if a.status == AgentStatus.READY:
            return a

    return None


def get_all_short(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[Dict[str, str]]:
    global _AGENTS_ONLINE

    list_agents_filters = []

    if list(_AGENTS_ONLINE.values()):

        list_agents_filters = list(_AGENTS_ONLINE.values())

        if filter:
            list_agents_filters = [
                a
                for a in list(_AGENTS_ONLINE.values())
                if filter in a.host or filter in str(a.id) or filter in str(a.port) or filter in a.status.value or filter in a.type
            ]

        if size and page:
            list_agents_filters = list_agents_filters[(
                page-1)*size:page*size]

        if order:
            list_agents_filters.sort(key=lambda a: getattr(a, order))

    return [
        {
            "id": n.id,
            "host": n.host,
            "port": n.port,
            "type": n.type
        }
        for n in list_agents_filters
    ]


def change_status(id: str, status: AgentStatus):
    agent = get(id)
    if agent:
        agent.status = status


def list_types() -> List[str]:
    global _AGENTS_TYPES
    return _AGENTS_TYPES


def add_agent_type(type: str):
    global _AGENTS_TYPES

    type = type.upper().lstrip()

    if type not in _AGENTS_TYPES:
        _AGENTS_TYPES.append(type)


def delete_agent_type(type: str):
    global _AGENTS_TYPES, _AGENTS_ONLINE

    type = type.upper().lstrip()

    agents_types_online = [
        a.type
        for a in _AGENTS_ONLINE.values()
    ]

    if type in _AGENTS_TYPES and type not in agents_types_online:
        _AGENTS_TYPES.remove(type)
