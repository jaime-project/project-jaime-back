
from typing import Dict, List

import requests
from logic.apps.agents.errors.agent_error import AgentError
from logic.apps.agents.services import agent_service
from logic.apps.clusters.errors.cluster_error import ClusterError
from logic.apps.clusters.models.cluster_model import Cluster, ClusterType
from logic.apps.clusters.repositories import cluster_repository
from logic.libs.exception.exception import AppException


def add(server: Cluster):

    if cluster_repository.exist(server.name):
        msj = f"El server con nombre {server.name} ya existe"
        raise AppException(ClusterError.CLUSTER_ALREADY_EXISTS_ERROR, msj)

    cluster_repository.add(server)


def get(name: str) -> Cluster:

    if not cluster_repository.exist(name):
        return None

    return cluster_repository.get(name)


def list_all() -> List[str]:

    return [
        s.name
        for s in cluster_repository.get_all()
    ]


def get_all() -> List[Cluster]:
    return cluster_repository.get_all()


def get_all_short() -> List[Dict[str, str]]:

    return [
        {
            "name": s.name,
            "type": s.type.value,
            "url": s.url
        }
        for s in cluster_repository.get_all()
    ]


def delete(name: str):

    if not cluster_repository.exist(name):
        msj = f"El server con nombre {name} no existe"
        raise AppException(ClusterError.CLUSTER_NOT_EXISTS_ERROR, msj)

    cluster_repository.delete(name)


def list_types() -> str:
    return [e.value for e in ClusterType]


def test_server(name: str) -> Dict[str, str]:

    cluster = get(name)
    agents = agent_service.get_by_type(cluster.type)
    if not agents:
        raise AppException(AgentError.AGENT_NOT_EXIST_ERROR,
                           "No hay agentes para la tarea")

    url = agents[0].get_url()
    json = {
        'url': cluster.url,
        'token': cluster.token,
        'type': cluster.type,
    }
    return requests.post(url=f'{url}/api/v1/jaime/cluster/test', json=json).json()


def modify(name: str, server: Cluster):
    delete(name)
    add(server)
