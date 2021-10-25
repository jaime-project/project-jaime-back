
from pathlib import Path
from typing import List

from logic.apps.filesystem.services import filesystem_service
from logic.apps.modules.errors.module_error import ModulesError
from logic.libs.exception.exception import AppException

_DEFAULT_RELATIVE_PATH = f'logic/apps/repo_modules_default'
_MODULES_PATH = f'{Path.home()}/.jaime/modules'


def add(name: str, content: str):

    path = f'{get_path()}/{name}.py'
    filesystem_service.create_file(path, content)


def get(name: str) -> str:

    path = f'{get_path()}/{name}.py'

    try:
        return filesystem_service.get_file_content(path).decode('utf-8')

    except Exception as e:
        raise AppException(
            code=ModulesError.MODULE_NO_EXIST_ERROR,
            exception=e,
            msj=f'El modulo {name} no existe o tiene un formato invalido'
        )


def list_all() -> List[str]:

    return [
        nf.replace('.py', '')
        for nf in filesystem_service.name_files_from_path(get_path())
        if not nf.endswith('.pyc')
    ]


def delete(name: str):

    try:
        get(name)

    except Exception:
        raise AppException(
            code=ModulesError.MODULE_NO_EXIST_ERROR,
            msj=f'El modulo {name} no existe o tiene un formato invalido'
        )

    path = f'{get_path()}/{name}.py'
    filesystem_service.delete_file(path)


def get_path() -> str:

    global _MODULES_PATH
    return _MODULES_PATH


def get_default_path() -> str:

    global _DEFAULT_RELATIVE_PATH
    return _DEFAULT_RELATIVE_PATH


def list_default() -> List[str]:

    return [
        nf.replace('.py', '')
        for nf in filesystem_service.name_files_from_path(get_default_path())
        if not nf.endswith('.pyc')
    ]
