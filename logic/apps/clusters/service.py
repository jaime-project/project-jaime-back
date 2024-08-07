
from typing import Dict, List

import requests

from logic.apps.agents import service as agent_service
from logic.apps.agents.error import AgentError
from logic.apps.clusters import repository
from logic.apps.clusters.error import ClusterError
from logic.apps.clusters.model import Cluster
from logic.libs.exception.exception import AppException


def add(cluster: Cluster):

    if repository.exist(cluster.name):
        msj = f"El cluster con nombre {cluster.name} ya existe"
        raise AppException(ClusterError.CLUSTER_ALREADY_EXISTS_ERROR, msj)

    repository.add(cluster)


def get(name: str) -> Cluster:

    if not repository.exist(name):
        return None

    return repository.get(name)


def list_all() -> List[str]:

    return [
        s.name
        for s in repository.get_all()
    ]


def get_all(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[Cluster]:
    return repository.get_all(size, page, filter, order)


def get_all_short(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[Dict[str, str]]:

    return [
        {
            "name": s.name,
            "url": s.url
        }
        for s in repository.get_all(size, page, filter, order)
    ]


def delete(name: str):

    if not repository.exist(name):
        msj = f"El server con nombre {name} no existe"
        raise AppException(ClusterError.CLUSTER_NOT_EXISTS_ERROR, msj)

    repository.delete(name)


def test_cluster(name: str, agent_type: str) -> Dict[str, str]:

    cluster = get(name)
    agents = agent_service.get_by_type(agent_type)
    if not agents:
        raise AppException(AgentError.AGENT_NOT_EXIST_ERROR,
                           f"Agent {agent_type} type not found")

    url = agents[0].get_url()
    json = {
        'url': cluster.url,
        'token': cluster.token,
        'type': agent_type
    }
    return requests.post(url=f'{url}/api/v1/jaime/clusters/test', json=json).json()


def modify(name: str, server: Cluster):
    delete(name)
    add(server)


def export_cluster(cluster_name: str) -> Dict[str, List[Dict[str, str]]]:

    objects = {}

    objects['clusters'] = [
        o.__dict__()
        for o in get_all()
        if o.name == cluster_name
    ]

    return objects
