
from typing import List

from logic.apps.docs.errors.doc_error import DocsError
from logic.apps.filesystem.services import filesystem_service
from logic.apps.modules.services import module_service
from logic.libs.exception.exception import AppException


def add(name: str, content: str, repo: str):

    path = f'{get_path()}/{repo}/{name}.yaml'
    filesystem_service.create_file(path, content)


def get(name: str, repo: str) -> str:

    path = f'{get_path()}/{repo}/{name}.yaml'

    try:
        return filesystem_service.get_file_content(path)

    except Exception as e:
        return None


def delete(name: str, repo: str):

    try:
        get(name, repo)

    except Exception:
        raise AppException(
            code=DocsError.DOC_NO_EXIST_ERROR,
            msj=f'La documentacion {name} no existe'
        )

    path = f'{get_path()}/{repo}/{name}.yaml'
    filesystem_service.delete_file(path)


def get_path() -> str:
    return module_service.get_path()


def list_all(repo: str) -> List[str]:

    return [
        nf.replace('.yaml', '')
        for nf in filesystem_service.name_files_from_path(f'{get_path()}/{repo}')
        if nf.endswith('.yaml')
    ]


def modify(name: str, content: str, repo: str):
    delete(name, repo)
    add(name, content, repo)
