import os
import shutil
from typing import List

from sqlalchemy import true


def get_file_content(path: str) -> str:
    with open(path, 'rb') as file:
        return file.read()


def create_file(path: str, content: str):
    with open(path, 'w+') as file:
        file.write(content)


def name_files_from_path(path: str) -> List[str]:
    result = []
    for _, _, name_files in os.walk(path):
        result += name_files
    return result


def delete_file(path: str):
    os.remove(path)


def delete_folder(path: str):
    shutil.rmtree(path, ignore_errors=True)


def move_file(path_in: str, path_out: str):
    shutil.move(path_in, path_out)
