import os
from importlib.util import module_from_spec, spec_from_file_location
import sys
from typing import Dict, List, Tuple
from uuid import UUID

from logic.apps.filesystem.services import workingdir_service
from logic.apps.modules.services import module_service
from logic.apps.works.errors.pipeline_error import WorkError
from logic.libs.exception.exception import AppException

from .garbage_collector import add_pipeline_runned


def exec(params: Dict[str, any]) -> UUID:

    id = workingdir_service.create()

    original_workindir = os.getcwd()
    workindir = workingdir_service.fullpath(id)

    original_stdout = sys.stdout
    logs_path = os.path.join(workindir, 'logs.log')

    try:
        module_name = params['module']
        module_path = os.path.join(
            module_service.get_path(), module_name + '.py')

        spec = spec_from_file_location(module_name, module_path)
        module = module_from_spec(spec)
        spec.loader.exec_module(module)

        os.chdir(workindir)
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

    add_pipeline_runned(id)

    return id
