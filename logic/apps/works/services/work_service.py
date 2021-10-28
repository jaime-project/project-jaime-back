import logging
import os
import sys
from datetime import datetime
from importlib.util import module_from_spec, spec_from_file_location
from multiprocessing import Process
from typing import Dict, List
from uuid import uuid4

from logic.apps.filesystem.services import workingdir_service
from logic.apps.modules.services import module_service
from logic.apps.modules.errors.module_error import ModulesError
from logic.apps.works.errors.work_error import WorkError
from logic.apps.works.models.work_model import Status, WorkStatus
from logic.libs.exception.exception import AppException

_LOGS_FILE_NAME = 'logs.log'
_WORKS_RUNNING: Dict[str, WorkStatus] = {}


def start(params: Dict[str, object]) -> str:

    id = _generate_id()
    work = Process(target=_exec, args=(params, id))

    global _WORKS_RUNNING
    _WORKS_RUNNING[id] = WorkStatus(work, id)

    work.start()

    return id


def get(id: str) -> WorkStatus:
    global _WORKS_RUNNING

    work = _WORKS_RUNNING.get(id, None)

    if not work.process.is_alive:
        finish_work(work.id)

    return work


def delete(id: str):
    global _WORKS_RUNNING

    worker = get(id)
    if not worker:
        msj = f"No existe worker con id {id}"
        raise AppException(ModulesError.MODULE_NO_EXIST_ERROR, msj)

    if worker.process.is_alive:
        worker.process.kill()

    _WORKS_RUNNING = {
        k: v
        for k, v in _WORKS_RUNNING.items()
        if k != id
    }

    workingdir_service.delete(id)


def list_all_running() -> List[str]:
    global _WORKS_RUNNING
    return _WORKS_RUNNING.keys()


def finish_work(id: str, status: Status):
    global _WORKS_RUNNING
    work = _WORKS_RUNNING[id]
    work.end_date = datetime.now()
    work.status = Status.TERMINATED


def _generate_id() -> str:
    return str(uuid4()).split('-')[4]


def _exec(params: Dict[str, object], id: str = str(uuid4())):

    if not params:
        msj = "Error al parsear los parametros"
        raise AppException(WorkError.EXECUTE_WORK_ERROR, msj)

    workingdir_service.create_by_id(id)

    original_workindir = os.getcwd()
    workindir_path = workingdir_service.fullpath(id)

    original_stdout = sys.stdout
    logs_path = os.path.join(workindir_path, _LOGS_FILE_NAME)
    logs_file = open(logs_path, 'w')

    error = None
    try:
        module_name = params['module']
        module_path = os.path.join(
            module_service.get_path(), module_name + '.py')

        spec = spec_from_file_location(module_name, module_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        os.chdir(workindir_path)
        sys.stdout = logs_file

        module.exec(params)

        os.chdir(original_workindir)
        sys.stdout = original_stdout
        logs_file.close()

    except AppException as ae:
        error = ae
        logging.exception(ae)

    except Exception as e:
        msj = str(e)
        error = AppException(WorkError.EXECUTE_WORK_ERROR, msj, e)
        logging.exception(error)

    finally:
        os.chdir(original_workindir)
        sys.stdout = original_stdout

    if error:
        raise error


def get_logs(id: str) -> str:

    log_path = os.path.join(workingdir_service.fullpath(id), _LOGS_FILE_NAME)

    if not os.path.exists(log_path):
        msj = f"No existe el log para el id {id}"
        raise AppException(WorkError.WORK_NOT_EXIST_ERROR, msj)

    with open(log_path, 'r') as f:
        content = f.read()

    return content
