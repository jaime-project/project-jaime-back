
import os
from typing import List

from logic.apps.filesystem import filesystem_service
from logic.apps.markdown.error import MarkdownError
from logic.apps.repos import service as repo_service
from logic.libs.exception.exception import AppException


def add(name: str, content: str, repo: str):

    path = f'{repo_service.get_repo_path(repo)}/{name}.md'

    if os.path.exists(path):
        msj = f"Markdown with name {name} already exist"
        raise AppException(MarkdownError.MARKDOWN_ALREADY_EXIST_ERROR, msj)

    filesystem_service.create_file(path, content)


def get(name: str, repo: str) -> str:

    path = f'{repo_service.get_repo_path(repo)}/{name}.md'

    try:
        return filesystem_service.get_file_content(path)

    except Exception as e:
        return None


def list_all(repo_name: str) -> List[str]:

    return [
        nf.replace('.md', '')
        for nf in filesystem_service.name_files_from_path(f'{repo_service.get_repo_path(repo_name)}')
        if nf.endswith('.md')
    ]


def delete(name: str, repo: str):

    try:
        get(name, repo)

    except Exception:
        raise AppException(
            code=MarkdownError.MARKDOWN_NO_EXIST_ERROR,
            msj=f'Markdown with name {name} not exist or this have a invalid format'
        )

    path = f'{repo_service.get_repo_path(repo)}/{name}.md'
    filesystem_service.delete_file(path)


def modify(name: str, content: str, repo: str):
    delete(name, repo)
    add(name, content, repo)
