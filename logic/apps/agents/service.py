from typing import Dict, List

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
        logger.log.warning(f'Ya existe un agente con el id {agent.id}')

    _AGENTS_ONLINE[agent.id] = agent

    add_agent_type(agent.type)

    service.update_requirements(service.get_requirements())
    logger.log.info(f'Nuevo agente conectado -> id: {str(agent.id)}')


def delete(id: str):

    try:
        disconnec_agent(id)
    except Exception as e:
        logger.log.error(e)

    agent_type = get(id).type

    global _AGENTS_ONLINE
    _AGENTS_ONLINE.pop(id)

    delete_agent_type(agent_type)


def disconnec_agent(id):

    agent = get(id)
    url = agent.get_url() + '/api/v1/jaime/'
    requests.delete(url)


def get(id: str) -> Agent:
    global _AGENTS_ONLINE
    return _AGENTS_ONLINE.get(id, None)


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
        msj = f'No hay agentes de tipo {type} desponibles'
        raise AppException(AgentError.AGENT_NOT_EXIST_ERROR, msj)

    for a in agents:
        if a.status == AgentStatus.READY:
            return a

    return None


def get_all_short() -> List[Dict[str, str]]:
    global _AGENTS_ONLINE

    return [
        {
            "id": n.id,
            "host": n.host,
            "port": n.port,
            "type": n.type
        }
        for _, n in list(_AGENTS_ONLINE.items())
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
