import os
from pathlib import Path
from typing import Dict, List
from datetime import datetime
import requests

from logic.apps.agents import service as agent_service
from logic.apps.agents.error import AgentError
from logic.apps.clusters import service
from logic.apps.clusters.model import Cluster
from logic.apps.configs import repository
from logic.apps.configs.error import ObjectError
from logic.apps.docs import service as doc_service
from logic.apps.filesystem import filesystem_service
from logic.apps.messages import service as message_service
from logic.apps.messages.model import Message, Status
from logic.apps.modules import service as module_service
from logic.apps.repos import service as repo_service
from logic.apps.repos.model import Repo, RepoGit
from logic.apps.servers import service as server_service
from logic.apps.servers.model import Server
from logic.libs.exception.exception import AppException
from logic.libs.logger import logger

_REQUIREMENTS_FILE_PATH = f'{Path.home()}/.jaime/requirements.txt'
_LOGS_FILE_PATH = f'{Path.home()}/.jaime/logs/app.log'


def update_requirements(content: str):

    filesystem_service.delete_file(get_requirements_path())
    filesystem_service.create_file(get_requirements_path(), content)

    for agent in agent_service.list_all():

        try:
            url = f'{agent.get_url()}/api/v1/configs/requirements'
            requests.post(url, data=content, verify=False)

        except Exception:
            logger.log.error(
                f'Error al conectarse al agente para actualizar las dependencias de pip')


def get_requirements() -> str:

    if not os.path.exists(get_requirements_path()):
        filesystem_service.create_file(get_requirements_path(), '')

    return filesystem_service.get_file_content(get_requirements_path())


def get_requirements_path() -> str:

    global _REQUIREMENTS_FILE_PATH
    return _REQUIREMENTS_FILE_PATH


def get_jaime_logs() -> str:
    return filesystem_service.get_file_content(_LOGS_FILE_PATH)


def get_agent_logs(agent_id: str) -> str:

    agent = agent_service.get(agent_id)
    if not agent:
        raise AppException(AgentError.AGENT_NOT_EXIST_ERROR,
                           f'El agente con id {agent_id} no existe')

    url = agent.get_url() + f'/api/v1/configs/logs'
    response = requests.get(url, verify=False)

    return response.text


def get_configs_vars() -> Dict[str, str]:
    return repository.get_all()


def update_configs_vars(dict: Dict[str, str]):
    for k, v in dict.items():
        repository.delete(k)
        repository.add(k, v)


def get_config_var(var: str) -> str:
    return get_configs_vars().get(var, None)


def update_config_var(var: str, value: str):
    update_configs_vars({var: value})


def exist_config_var(var: str) -> bool:
    return repository.exist(var)


def get_all_objects() -> Dict[str, List[Dict[str, str]]]:

    objects = {}

    objects['servers'] = [
        o.__dict__()
        for o in server_service.get_all()
    ]

    objects['clusters'] = [
        o.__dict__()
        for o in service.get_all()
    ]

    objects['repos'] = [
        o.__dict__()
        for o in repo_service.get_all()
    ]

    objects['modules'] = []
    for repo in objects['repos']:
        for module_name in module_service.list_all(repo['name']):

            objects['modules'].append({
                'repo': repo['name'],
                'name': module_name,
                'content': module_service.get(module_name, repo['name'])
            })

    objects['docs'] = []
    for repo in objects['repos']:
        for doc_name in doc_service.list_all(repo['name']):

            objects['docs'].append({
                'repo': repo['name'],
                'name': doc_name,
                'content': doc_service.get(doc_name, repo['name'])
            })

    objects['requirements'] = get_requirements()

    objects['configs'] = get_configs_vars()

    objects['messages'] = [m.__dict__() for m in message_service.get_all()]

    return objects


def update_objects(objects: Dict[str, str], replace: bool = False):

    try:
        _create_and_update_objects(objects, replace)

    except Exception as e:
        raise AppException(ObjectError.CREATION_OBJECTS_ERROR, str(e), e)


def _create_and_update_objects(objects: Dict[str, str], replace: bool):

    if 'clusters' in objects:

        for o in objects['clusters']:

            cluster = Cluster(
                name=o['name'],
                url=o['url'],
                token=o['token'],
                type=o['type'],
                version=o['version']
            )

            if replace and service.get(cluster.name):
                service.delete(cluster.name)
                service.add(cluster)

            if not service.get(cluster.name):
                service.add(cluster)

    if 'servers' in objects:

        for o in objects['servers']:

            server = Server(
                name=o['name'],
                host=o['host'],
                port=o['port'],
                user=o['user'],
                password=o['password'],
            )

            if replace and server_service.get(server.name):
                server_service.delete(server.name)
                server_service.add(server)

            if not server_service.get(server.name):
                server_service.add(server)

    if 'repos' in objects:

        for o in objects['repos']:

            repo = Repo(
                name=o['name'],
            )

            if 'git_url' in o:
                repo = RepoGit(
                    name=o['name'],
                    git_path=o['git_path'],
                    git_user=o['git_user'],
                    git_pass=o['git_pass'],
                    git_url=o['git_url'],
                    git_branch=o['git_branch'],
                )

            if replace and repo_service.get(repo.name):
                repo_service.delete(repo.name)
                repo_service.add(repo)

            if not repo_service.get(repo.name):
                repo_service.add(repo)

    if 'modules' in objects:

        for o in objects['modules']:

            name = o['name']
            content = o['content']
            repo = o['repo']

            if replace and module_service.get(name, repo):
                module_service.delete(name, repo)
                module_service.add(name, content, repo)

            if not module_service.get(name, repo):
                module_service.add(name, content, repo)

    if 'docs' in objects:
        for o in objects['docs']:

            name = o['name']
            content = o['content']
            repo = o['repo']

            if replace and doc_service.get(name, repo):
                doc_service.delete(name, repo)
                doc_service.add(name, content, repo)

            if not doc_service.get(name, repo):
                doc_service.add(name, content, repo)

    if 'requirements' in objects:
        update_requirements(objects['requirements'])

    if 'configs' in objects:
        update_configs_vars(objects['configs'])

    if 'messages' in objects:
        for m in objects['messages']:

            message = Message(
                id=m['id'],
                title=m['title'],
                subject=m['subject'],
                body=m['body'],
                job=m['job'],
                status=Status(m['status']),
                date=datetime.fromisoformat(m['date']),
                files=m.get('files', []),
            )

            if replace:
                if message_service.get(message.id):
                    message_service.delete(message.id)

            message_service.add(message)
