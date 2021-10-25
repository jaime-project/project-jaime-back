from datetime import datetime
from threading import Thread
from typing import Dict, List
from uuid import uuid4

from logic.apps.processes.models.process_model import ProcessStatus, Status
from logic.apps.works.services import work_service
from logic.libs.logger.logger import logger

_PROCESS_RUNING: Dict[str, ProcessStatus] = {}


def run(params: Dict[str, object]) -> str:

    id = generate_id()
    process = Thread(target=work_service.exec, args=(params, id))

    global _PROCESS_RUNING
    _PROCESS_RUNING[id] = ProcessStatus(process)

    process.start()

    return id


def kill(id: str):
    global _PROCESS_RUNING

    processStatus = _PROCESS_RUNING[id]

    if processStatus.thread.is_alive():
        processStatus.thread.setDaemon(False)

    delete_from_list(id)


def list_all_running() -> List[str]:
    global _PROCESS_RUNING
    return _PROCESS_RUNING.keys()


def generate_id() -> str:
    return str(uuid4()).split('-')[4]


def delete_from_list(id: str):
    global _PROCESS_RUNING
    _PROCESS_RUNING = {
        k: v
        for k, v in _PROCESS_RUNING.items()
        if k != id
    }


def finish_process_success(id: str):
    _finish_process(id, Status.SUCCESS)


def finish_process_error(id: str):
    _finish_process(id, Status.ERROR)


def _finish_process(id: str, status: Status):
    global _PROCESS_RUNING
    process = _PROCESS_RUNING[id]
    process.end_date = datetime.now()
    process.status = status


def get(id: str) -> ProcessStatus:
    global _PROCESS_RUNING
    return _PROCESS_RUNING[id]
