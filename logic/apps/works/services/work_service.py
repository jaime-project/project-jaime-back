import os
import sys
from importlib.util import module_from_spec, spec_from_file_location
from multiprocessing import context
from typing import Any, Dict
from uuid import UUID, uuid4

from logic.apps.filesystem.services import workingdir_service
from logic.apps.modules.services import module_service
from logic.apps.processes.services import process_service
from logic.apps.works.errors.work_error import WorkError
from logic.libs.exception.exception import AppException

from .garbage_collector import add_work_runned

_LOGS_FILE_NAME = 'logs.log'


def exec(params: Dict[str, object], id: str = str(uuid4())) -> Any:

    workingdir_service.create_by_id(id)

    original_workindir = os.getcwd()
    workindir_path = workingdir_service.fullpath(id)

    original_stdout = sys.stdout
    logs_path = os.path.join(workindir_path, _LOGS_FILE_NAME)

    try:
        module_name = params['module']
        module_path = os.path.join(
            module_service.get_path(), module_name + '.py')

        spec = spec_from_file_location(module_name, module_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        os.chdir(workindir_path)
        with open(logs_path, 'w') as f:
            sys.stdout = f

        module.exec(params)

        os.chdir(original_workindir)
        sys.stdout = original_stdout

    except Exception as e:

        os.chdir(original_workindir)
        sys.stdout = original_stdout
        workingdir_service.delete(id)

        msj = str(e)
        raise AppException(WorkError.EXECUTE_WORK_ERROR, msj, e)

    add_work_runned(id)

    return id


def get_logs(id: str) -> str:

    log_path = os.path.join(workingdir_service.fullpath(id), _LOGS_FILE_NAME)
    with open(log_path, 'r') as f:
        content = f.read()

    return content


def stop_work(id: str):
    process_service.kill(id)
    workingdir_service.delete(id)
