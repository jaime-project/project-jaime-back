
from pathlib import Path
from typing import List

from logic.apps.filesystem.services import filesystem_service
from logic.apps.modules.errors.module_error import ModulesError
from logic.libs.exception.exception import AppException

_MODULES_PATH = f'{Path.home()}/.jaime/modules'


def add(name: str, content: str, repo: str):

    path = f'{get_path()}/{repo}/{name}.py'
    filesystem_service.create_file(path, content)


def get(name: str, repo: str) -> str:

    path = f'{get_path()}/{repo}/{name}.py'

    try:
        return filesystem_service.get_file_content(path).decode('utf-8')

    except Exception as e:
        return None


def list_all(repo_name: str) -> List[str]:

    return [
        nf.replace('.py', '')
        for nf in filesystem_service.name_files_from_path(f'{get_path()}/{repo_name}')
        if nf.endswith('.py')
    ]


def delete(name: str, repo: str):

    try:
        get(name, repo)

    except Exception:
        raise AppException(
            code=ModulesError.MODULE_NO_EXIST_ERROR,
            msj=f'El modulo {name} no existe o tiene un formato invalido'
        )

    path = f'{get_path()}/{repo}/{name}.py'
    filesystem_service.delete_file(path)


def get_path() -> str:

    global _MODULES_PATH
    return _MODULES_PATH


def modify(name: str, content: str, repo: str):
    delete(name, repo)
    add(name, content, repo)
