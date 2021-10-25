import os
import sys
from importlib.util import module_from_spec, spec_from_file_location
from typing import Dict
from uuid import UUID, uuid4

from logic.apps.filesystem.services import workingdir_service
from logic.apps.modules.services import module_service
from logic.apps.processes.services import process_service
from logic.apps.works.errors.work_error import WorkError
from logic.libs.exception.exception import AppException

_LOGS_FILE_NAME = 'logs.log'


def exec(params: Dict[str, object], id: str = str(uuid4())):

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

    except Exception as e:
        msj = str(e)
        error = AppException(WorkError.EXECUTE_WORK_ERROR, msj, e)

    finally:
        os.chdir(original_workindir)
        sys.stdout = original_stdout

    if error:
        process_service.finish_process_error(id)
        raise error

    process_service.finish_process_success(id)


def get_logs(id: str) -> str:

    log_path = os.path.join(workingdir_service.fullpath(id), _LOGS_FILE_NAME)

    if not os.path.exists(log_path):
        msj = f"No existe el log para el id {id}"
        raise AppException(WorkError.WORK_NOT_EXIST_ERROR, msj)

    with open(log_path, 'r') as f:
        content = f.read()

    return content
