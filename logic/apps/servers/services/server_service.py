
from pathlib import Path
from typing import List

from logic.apps.filesystem.services import filesystem_service
from logic.apps.servers.errors.server_error import ServerError
from logic.libs.exception.exception import AppException

_TEMPLATES_PATH = f'{Path.home()}/.jaime/servers'


def add(name: str, content: str):

    path = f'{get_path()}/{name}.txt'
    filesystem_service.create_file(path, content)


def get(name: str) -> str:

    path = f'{get_path()}/{name}.txt'
    try:
        return filesystem_service.get_file_content(path).decode('utf-8')

    except Exception as e:
        raise AppException(
            code=ServerError.TEMPLATE_NOT_EXISTS_ERROR,
            exception=e,
            msj=f'El modulo {name} no existe o tiene un formato invalido'
        )


def list_all() -> List[str]:

    return [
        nf.replace('.txt', '')
        for nf in filesystem_service.name_files_from_path(get_path())
    ]


def delete(name: str):

    path = f'{get_path()}/{name}.txt'
    filesystem_service.delete_file(path)


def get_path() -> str:

    global _TEMPLATES_PATH
    return _TEMPLATES_PATH
