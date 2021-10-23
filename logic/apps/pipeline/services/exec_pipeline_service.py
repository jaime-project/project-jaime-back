import os
from importlib.util import module_from_spec, spec_from_file_location
from typing import Dict, List, Tuple
from uuid import UUID

from logic.apps.filesystem.services import workingdir_service
from logic.apps.modules.services import module_service
from logic.apps.pipeline.errors.pipeline_error import PipelineError
from logic.libs.exception.exception import AppException

from .garbage_collector import add_pipeline_runned


def exec(pipeline: List[Dict[str, any]]) -> UUID:

    id = workingdir_service.create()

    try:
        original_workindir = os.getcwd()
        workindir = workingdir_service.fullpath(id)
        os.chdir(workindir)

        for stage in pipeline:

            module_name = stage['module']
            module_path = f'{module_service.get_path()}/{module_name}.py'

            spec = spec_from_file_location(module_name, module_path)
            module = module_from_spec(spec)
            spec.loader.exec_module(module)

            module.exec(workindir, stage)

        os.chdir(original_workindir)

    except Exception as e:

        os.chdir(original_workindir)
        workingdir_service.delete(id)

        msj = str(e)
        raise AppException(PipelineError.EXECUTE_PIPELINE_ERROR, msj, e)

    add_pipeline_runned(id)

    return id
