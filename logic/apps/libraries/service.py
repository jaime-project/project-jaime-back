import os
from pathlib import Path
from typing import Dict, List

from logic.apps.admin.configs.variables import Vars
from logic.apps.libraries import repository
from logic.apps.libraries.error import LibraryError
from logic.apps.libraries.model import Library
from logic.libs.exception.exception import AppException
from logic.libs.logger import logger
from logic.libs.variables.variables import get_var


def add(library: Library):

    if repository.exist(library.name):
        msj = f"Library with name {library.name} already exist"
        raise AppException(LibraryError.LIBRARY_ALREADY_EXISTS_ERROR, msj)

    repository.add(library)
    load_library(library)


def get(name: str) -> Library:

    if not repository.exist(name):
        return None

    return repository.get(name)


def list_all() -> List[str]:

    return [
        s.name
        for s in repository.get_all()
    ]


def get_all(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[Library]:
    return repository.get_all(size, page, filter, order)


def get_all_short(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[Dict[str, str]]:

    return [
        {
            "name": s.name,
            "description": s.description,
            "repo": s.repo
        }
        for s in repository.get_all(size, page, filter, order)
    ]


def delete(name: str):

    if not repository.exist(name):
        msj = f"Library with name {name} not exist"
        raise AppException(LibraryError.LIBRARY_NOT_EXISTS_ERROR, msj)

    repository.delete(name)


def modify(name: str, server: Library):
    delete(name)
    add(server)


def get_path() -> str:
    return f'{get_var(Vars.JAIME_HOME_PATH)}/libraries'


def load_library(library: Library):

    out_path = f'{get_path()}/{library.name}'
    os.system(f'rm -rf {out_path}/*')

    if not os.path.exists(out_path):
        Path(out_path).mkdir(parents=True)

    url = library.repo

    if library.user and library.password:
        repo_git_without_https = library.repo.replace("https://", "")
        url = f'https://{library.user}:{library.password}@{repo_git_without_https}'

    logger.log.info('Creating directories for git clone')
    tmp_path = '/tmp'
    os.system(f'rm -fr {tmp_path}/{library.name}')

    logger.log.info(
        f'Cloning library -> repo:{library.repo} branch:{library.branch} user:{library.user}')
    os.system(f'git clone {url} {tmp_path}/{library.name} -b {library.branch}')

    in_path = f'{tmp_path}/{library.name}/{library.path}'.replace('//', '/')

    os.system(f'mv {in_path}/* {out_path}')


def load_libraries_in_workingdir(workingdir_path: str):

    for library_name in list_all():

        library_path = f'{get_path()}/{library_name}'
        os.system(f'cp -rf {library_path}/*.py {workingdir_path}')


def delete_libraries_in_workingdir(workingdir_path: str):
    os.system(f'rm -fr {workingdir_path}/*.py')
