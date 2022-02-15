
import os
from pathlib import Path
from typing import Dict, List

from logic.apps.modules.services import module_service
from logic.apps.repos.errors.repo_error import RepoError
from logic.apps.repos.models.repo_model import RepoGit, Repo, RepoType
from logic.apps.repos.repositories import repo_repository
from logic.libs.exception.exception import AppException

_REPOS_PATH = f'{Path.home()}/.jaime/modules'


def add(repo: Repo):

    if repo_repository.exist(repo.name):
        msj = f"El repo con nombre {repo.name} ya existe"
        raise AppException(RepoError.REPO_ALREADY_EXISTS_ERROR, msj)

    repo_repository.add(repo)


def get(name: str) -> Repo:

    if not repo_repository.exist(name):
        return None

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


def get_all() -> List[str]:
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


def modify(name: str, repo: RepoGit):
    delete(name)
    add(repo)


def update_git_repo(repo: RepoGit):

    tmp_path = '/temp'
    repo_name = _get_git_repo_name(repo.git_url)
    in_path = f'{tmp_path}/{repo_name}'
    os.system(f'rm -fr {in_path}')

    download_git_repo(repo)


def download_git_repo(repo: RepoGit):

    if repo.type != RepoType.GIT:
        return

    repo_name = _get_git_repo_name(repo.git_url)
    repo_git_without_https = repo.git_url.replace("https://", "")

    url = f'https://{repo.git_user}:{repo.git_pass}@{repo_git_without_https}'
    tmp_path = '/temp'
    os.system(f'git clone {url} {tmp_path}')

    in_path = f'{tmp_path}/{repo_name}/{repo.git_path}'
    out_path = f'{module_service.get_path()}/{repo.name}'
    if not Path.exists(out_path):
        os.mkdir(out_path)
    os.system(f'mv -rf {in_path} {out_path}')


def is_downloaded(name: str) -> bool:
    module_path = f'{module_service.get_path()}/{name}'
    return os.path.exists(module_path)


def _get_git_repo_name(repo_url: str) -> str:
    return repo_url.split('/')[-1].replace('.git', '')
