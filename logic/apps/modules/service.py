
import os
from pathlib import Path
from typing import List

from logic.apps.filesystem import filesystem_service
from logic.apps.modules.error import ModulesError
from logic.apps.repos import service as repo_service
from logic.libs.exception.exception import AppException


def add(name: str, content: str, repo: str):

    path = f'{repo_service.get_repo_path(repo)}/{name}.py'

    if os.path.exists(path):
        msj = f"Module with name {name} already exist"
        raise AppException(ModulesError.MODULE_ALREADY_EXIST_ERROR, msj)

    filesystem_service.create_file(path, content)


def get(name: str, repo: str) -> str:

    path = f'{repo_service.get_repo_path(repo)}/{name}.py'

    try:
        return filesystem_service.get_file_content(path)

    except Exception as e:
        return None


def list_all(repo_name: str) -> List[str]:

    return [
        nf.replace('.py', '')
        for nf in filesystem_service.name_files_from_path(f'{repo_service.get_repo_path(repo_name)}')
        if nf.endswith('.py')
    ]


def delete(name: str, repo: str):

    try:
        get(name, repo)

    except Exception:
        raise AppException(
            code=ModulesError.MODULE_NO_EXIST_ERROR,
            msj=f'Module with name {name} not exist or this have a invalid format'
        )

    path = f'{repo_service.get_repo_path(repo)}/{name}.py'
    filesystem_service.delete_file(path)


def modify(name: str, content: str, repo: str):
    delete(name, repo)
    add(name, content, repo)
