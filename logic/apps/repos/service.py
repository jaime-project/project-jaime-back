
import os

from logic.apps.admin.configs.variables import Vars, get_var
from logic.apps.docs import service as doc_service
from logic.apps.filesystem import filesystem_service
from logic.apps.jobs.model import Job
from logic.apps.markdown import service as markdown_service
from logic.apps.modules import service as module_service
from logic.apps.repos import repository
from logic.apps.repos.error import RepoError
from logic.apps.repos.model import Repo, RepoGit, RepoType
from logic.libs.exception.exception import AppException
from logic.libs.logger import logger


def add(repo: Repo):

    if repository.exist(repo.name):
        msj = f"Repository with name {repo.name} already exists"
        raise AppException(RepoError.REPO_ALREADY_EXISTS_ERROR, msj)

    if repo.type == RepoType.GIT:
        clone_repo_git(repo)

    repository.add(repo)


def get(name: str) -> Repo:
    return repository.get(name)


def list_all() -> list[str]:

    return [
        s.name
        for s in repository.get_all()
    ]


def list_all_by_type(type: RepoType) -> list[str]:

    return [
        s.name
        for s in repository.get_all()
        if s.type == type
    ]


def get_all() -> list[Repo]:
    return repository.get_all()


def get_all_short() -> list[dict[str, str]]:

    return [
        {
            "name": s.name,
            "type": s.type.value,
            "url": s.git_url
        }
        for s in repository.get_all()
    ]


def delete(name: str):

    if not repository.exist(name):
        msj = f"Repository with name {name} not exists"
        raise AppException(RepoError.REPO_NOT_EXISTS_ERROR, msj)

    repository.delete(name)
    filesystem_service.delete_folder(f'{_get_base_path()}/{name}')


def modify(name: str, repo: RepoGit):
    delete(name)
    add(repo)


def clone_repo_git(repo_git: RepoGit) -> str:

    repo_full_path = f'{_get_base_path()}/{repo_git.name}'

    logger.log.info(f'Making directories for git clone -> {repo_full_path}')
    os.system(f'rm -rf {repo_full_path}')
    os.system(f'mkdir -p {repo_full_path}')

    url = repo_git.git_url

    if repo_git.git_user and repo_git.git_pass:
        repo_git_without_https = repo_git.git_url.replace("https://", "")
        url = f'https://{repo_git.git_user}:{repo_git.git_pass}@{repo_git_without_https}'

    logger.log.info(
        f'Making url for git clone -> {repo_git.git_url}')
    os.system(f'git clone -b {repo_git.git_branch} {url} {repo_full_path}')

    return repo_full_path


def commit_push_repo_git(repo_git: RepoGit, commit_message: str = "Updated by Jaime"):

    repo_full_path = f'{_get_base_path()}/{repo_git.name}'

    logger.log.info(f"Starting git push process to repo -> {repo_git.name}")
    os.system(f"""cd {repo_full_path}/{repo_git.git_path} && \ 
              git pull && \
              git add . && \
              git commit -m "{commit_message}" && \
              git push -u origin {repo_git.git_branch}""")


def pull_repo_git(repo_git: RepoGit):

    repo_full_path = f'{_get_base_path()}/{repo_git.name}'

    logger.log.info(f"Git pull to repo -> {repo_git.name}")
    os.system(f"cd {repo_full_path} && git pull")


def list_types() -> list[str]:
    return [e.value for e in RepoType]


def export_repo(repo_name: str) -> dict[str, list[dict[str, str]]]:

    objects = {}

    objects['repos'] = [
        o.__dict__()
        for o in get_all()
        if o.name == repo_name
    ]

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

    objects['markdowns'] = []
    for markdown_name in markdown_service.list_all(repo_name):

        objects['markdowns'].append({
            'repo': repo_name,
            'name': markdown_name,
            'content': markdown_service.get(markdown_name, repo_name)
        })

    return objects


def export_repo_zip(repo_name: str) -> bytes:

    tar_path = f'/tmp/{repo_name}.tar.gz'

    os.system(
        f"cd {_get_base_path()} && tar -zcvf {tar_path} {repo_name}")

    return open(tar_path, 'rb').read()


def _get_base_path() -> str:
    return f'{get_var(Vars.JAIME_HOME_PATH)}/repos'


def get_repo_path(repo_name: str) -> str:

    repo = get(repo_name)

    if repo.type == RepoType.GIT:
        return f'{_get_base_path()}/{repo.name}/{repo.git_path}'

    return f'{_get_base_path()}/{repo.name}'


def get_module_path_of_job(job: Job) -> str:
    return f"{get_repo_path(job.module_repo)}/{job.module_name}.py"
