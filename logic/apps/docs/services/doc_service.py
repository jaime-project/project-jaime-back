
from pathlib import Path
from typing import List

from logic.apps.filesystem.services import filesystem_service
from logic.apps.docs.errors.doc_error import DocsError
from logic.libs.exception.exception import AppException

_DEFAULT_RELATIVE_PATH = f'repo_docs_default'
_DOCS_PATH = f'{Path.home()}/.jaime/docs'


def add(name: str, content: str):

    path = f'{get_path()}/{name}.yaml'
    filesystem_service.create_file(path, content)


def get(name: str) -> str:

    path = f'{get_path()}/{name}.yaml'

    try:
        return filesystem_service.get_file_content(path).decode('utf-8')

    except Exception as e:
        raise AppException(
            code=DocsError.DOC_NO_EXIST_ERROR,
            exception=e,
            msj=f'La documentacion {name} no existe'
        )


def list_all() -> List[str]:

    return [
        nf.replace('.yaml', '')
        for nf in filesystem_service.name_files_from_path(get_path())
    ]


def delete(name: str):

    try:
        get(name)

    except Exception:
        raise AppException(
            code=DocsError.DOC_NO_EXIST_ERROR,
            msj=f'La documentacion {name} no existe'
        )

    path = f'{get_path()}/{name}.yaml'
    filesystem_service.delete_file(path)


def get_path() -> str:

    global _DOCS_PATH
    return _DOCS_PATH


def get_default_path() -> str:

    global _DEFAULT_RELATIVE_PATH
    return _DEFAULT_RELATIVE_PATH


def list_default() -> List[str]:

    return [
        nf.replace('.yaml', '')
        for nf in filesystem_service.name_files_from_path(get_default_path())
    ]
