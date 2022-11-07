
import os
from pathlib import Path
from typing import Dict, List

from logic.apps.docs.services import doc_service
from logic.apps.filesystem.services import filesystem_service
from logic.apps.modules.services import module_service
from logic.apps.repos.errors.repo_error import RepoError
from logic.apps.repos.models.repo_model import Repo, RepoGit, RepoType
from logic.apps.repos.repositories import repo_repository
from logic.libs.exception.exception import AppException
from logic.libs.logger.logger import logger


def add(repo: Repo):

    if repo_repository.exist(repo.name):
        msj = f"El repo con nombre {repo.name} ya existe"
        raise AppException(RepoError.REPO_ALREADY_EXISTS_ERROR, msj)

    repo_repository.add(repo)
    load_repo(repo)


def get(name: str) -> Repo:
    return repo_repository.get(name)


def list_all() -> List[str]:

    return [
        s.name
        for s in repo_repository.get_all()
    ]


def list_all_by_type(type: RepoType) -> List[str]:

    return [
        s.name
        for s in repo_repository.get_all()
        if s.type == type
    ]


def get_all() -> List[Repo]:
    return repo_repository.get_all()


def get_all_short() -> List[Dict[str, str]]:

    return [
        {
            "name": s.name,
            "type": s.type.value,
            "url": s.url
        }
        for s in repo_repository.get_all()
    ]


def delete(name: str):

    if not repo_repository.exist(name):
        msj = f"El repo con nombre {name} no existe"
        raise AppException(RepoError.REPO_NOT_EXISTS_ERROR, msj)

    repo_repository.delete(name)
    filesystem_service.delete_folder(f'{module_service.get_path()}/{name}')


def modify(name: str, repo: RepoGit):
    delete(name)
    add(repo)


def reload_repo_git(repo_name: str):

    repo = get(repo_name)

    tmp_path = '/tmp'
    repo_name = _get_git_repo_name(repo.git_url)
    in_path = f'{tmp_path}/{repo_name}'
    os.system(f'rm -fr {in_path}')

    load_repo(repo)


def load_repo(repo: Repo):

    out_path = f'{module_service.get_path()}/{repo.name}'

    if not os.path.exists(out_path):
        Path(out_path).mkdir(parents=True)

    if repo.type != RepoType.GIT:
        return

    repo_name = _get_git_repo_name(repo.git_url)
    url = repo.git_url

    if repo.git_user and repo.git_pass:
        repo_git_without_https = repo.git_url.replace("https://", "")
        url = f'https://{repo.git_user}:{repo.git_pass}@{repo_git_without_https}'

    logger().info(f'Creating directories for git clone')
    tmp_path = '/tmp'
    os.system(f'rm -fr {tmp_path}/{repo_name}')

    logger().info(
        f'Cloning repository -> {repo.git_url} -b {repo.git_branch} -u {repo.git_user}')
    os.system(f'git clone {url} {tmp_path}/{repo_name} -b {repo.git_branch}')

    in_path = f'{tmp_path}/{repo_name}/{repo.git_path}'.replace('//', '/')

    os.system(f'rm -rf {out_path}/*')
    os.system(f'mv {in_path}/* {out_path}')


def is_loaded(name: str) -> bool:
    module_path = f'{module_service.get_path()}/{name}'
    return os.path.exists(module_path)


def _get_git_repo_name(repo_url: str) -> str:
    return repo_url.split('/')[-1].replace('.git', '')


def list_types() -> List[str]:
    return [e.value for e in RepoType]


def export_modules_and_docs(repo_name: str) -> Dict[str, List[Dict[str, str]]]:

    objects = {}

    objects['repos'] = [repo_name]

    objects['modules'] = []
    for module_name in module_service.list_all(repo_name):

        objects['modules'].append({
            'repo': repo_name,
            'name': module_name,
            'content': module_service.get(module_name, repo_name)
        })

    objects['docs'] = []
    for doc_name in doc_service.list_all(repo_name):

        objects['docs'].append({
            'repo': repo_name,
            'name': doc_name,
            'content': doc_service.get(doc_name, repo_name)
        })

    return objects
