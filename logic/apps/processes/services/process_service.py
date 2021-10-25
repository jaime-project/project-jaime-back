from multiprocessing import Process
from typing import Dict, List

from logic.apps.works.services import work_service
from logic.libs.logger.logger import logger

_PROCESS_RUNING: Dict[str, Process] = {}


def run(params: Dict[str, object]) -> int:

    process = Process(target=work_service.exec, args=(params))

    global _PROCESS_RUNING
    _PROCESS_RUNING[process.pid] = process

    process.start()

    return process.pid


def kill(id: int):
    global _PROCESS_RUNING

    process = _PROCESS_RUNING[id]

    if process.is_alive():
        process.kill()


def alive(id: int) -> bool:
    global _PROCESS_RUNING
    process = _PROCESS_RUNING[id]

    return process.is_alive()


def processes_running() -> List[int]:
    global _PROCESS_RUNING
    return _PROCESS_RUNING.keys()
