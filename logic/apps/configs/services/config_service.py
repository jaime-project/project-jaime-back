import os
from pathlib import Path
from typing import Dict

import requests
from logic.apps.agents.services import agent_service
from logic.apps.clusters.models.cluster_model import Cluster
from logic.apps.clusters.services import cluster_service
from logic.apps.configs.errors.config_error import ObjectError
from logic.apps.docs.services import doc_service
from logic.apps.filesystem.services import filesystem_service
from logic.apps.modules.services import module_service
from logic.apps.repos.models.repo_model import Repo, RepoGit, RepoType
from logic.apps.repos.services import repo_service
from logic.apps.servers.models.server_model import Server
from logic.apps.servers.services import server_service
from logic.libs.exception.exception import AppException

_REQUIREMENTS_FILE_PATH = f'{Path.home()}/.jaime/requirements.txt'


def update_requirements(content: str):

    filesystem_service.delete_file(get_requirements_path())
    filesystem_service.create_file(get_requirements_path(), content)

    for agent in agent_service.list_all():

        url = f'{agent.get_url()}/api/v1/configs/requirements'
        requests.post(url, data=content, verify=False)


def get_requirements() -> str:

    if not os.path.exists(get_requirements_path()):
        filesystem_service.create_file(get_requirements_path(), '')

    return filesystem_service.get_file_content(get_requirements_path())


def get_requirements_path() -> str:

    global _REQUIREMENTS_FILE_PATH
    return _REQUIREMENTS_FILE_PATH


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

            if replace and cluster_service.get(cluster.name):
                cluster_service.delete(cluster.name)
                cluster_service.add(cluster)

            if not cluster_service.get(cluster.name):
                cluster_service.add(cluster)

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
