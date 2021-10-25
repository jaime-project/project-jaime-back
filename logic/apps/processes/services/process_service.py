from multiprocessing import Process
from typing import Dict, List
from uuid import UUID, uuid4

from logic.apps.works.services import work_service
from logic.libs.logger.logger import logger

_PROCESS_RUNING: Dict[str, Process] = {}


def run(params: Dict[str, object]) -> str:

    id = generate_id()
    process = Process(target=work_service.exec, args=(params, id))

    global _PROCESS_RUNING
    _PROCESS_RUNING[id] = process

    process.start()

    return id


def kill(id: str):
    global _PROCESS_RUNING

    process = _PROCESS_RUNING[id]

    if process.is_alive():
        process.kill()


def alive(id: str) -> bool:
    global _PROCESS_RUNING
    process = _PROCESS_RUNING[id]

    return process.is_alive()


def all_running() -> List[str]:
    global _PROCESS_RUNING
    return _PROCESS_RUNING.keys()


def generate_id() -> str:
    return str(uuid4()).split('-')[4]
