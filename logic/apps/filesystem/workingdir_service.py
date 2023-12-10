import os
import shutil
from pathlib import Path
from typing import Any, List
from uuid import UUID, uuid4

from logic.apps.admin.configs.variables import Vars, get_var
from logic.apps.jobs.model import Job

_NAME_FILE_LOGS = 'logs.log'


def create() -> UUID:
    id = uuid4()
    Path(fullpath(id)).mkdir(parents=True, exist_ok=True)
    return id


def create_by_id(id: Any):

    if Path.exists(Path(fullpath(id))):
        delete(id)

    Path(fullpath(id)).mkdir(parents=True, exist_ok=True)
    with open(f'{fullpath(id)}/{_NAME_FILE_LOGS}', 'w'):
        pass


def delete(id: Any):
    shutil.rmtree(fullpath(id))


def fullpath(id: Any) -> str:
    return os.path.join(get_var(Vars.WORKINGDIR_PATH), id)


def get(id: Any) -> List[str]:
    result = []
    for (dirpath, _, _) in os.walk(fullpath(id)):
        result.extend(dirpath)

    return result


def get_logs_path(id: str) -> str:
    return os.path.join(fullpath(id), _NAME_FILE_LOGS)
