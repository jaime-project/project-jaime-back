import shutil
from os import walk
from pathlib import Path
from typing import List
from uuid import UUID, uuid4

_TEMP_PATH = '/tmp'


def create() -> UUID:
    id = uuid4()
    Path(fullpath(id)).mkdir(parents=True, exist_ok=True)
    return id


def delete(id: UUID):
    shutil.rmtree(fullpath(id))


def fullpath(id: UUID) -> str:
    return f'{_TEMP_PATH}/{id}'


def get(id: UUID) -> List[str]:
    result = []
    for (dirpath, _, _) in walk(fullpath(id)):
        result.extend(dirpath)

    return result
