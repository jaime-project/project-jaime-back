import os
from typing import List
from zipfile import ZIP_DEFLATED, ZipFile

from logic.libs.logger import logger


def create(zip_path: str, file_paths: str):

    original_workindir = os.getcwd()
    os.chdir(file_paths)

    paths = walk_path(file_paths)
    with ZipFile(zip_path, 'w', ZIP_DEFLATED) as zip:
        for file in paths:
            zip.write(file.replace(f'{file_paths}/', '').replace('//', ''))

    os.chdir(original_workindir)


def walk_path(folder_path: str) -> List[str]:
    result = []
    for (dirpath, dirs, files) in os.walk(folder_path):

        for dir in dirs:
            result.append(os.path.join(dirpath, dir))

        for file in files:
            result.append(os.path.join(dirpath, file))

    return result
