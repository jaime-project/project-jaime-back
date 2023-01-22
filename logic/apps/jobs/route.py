from datetime import datetime
from typing import Dict

import yaml
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.responses import Response

from logic.apps.agents import service as agent_service
from logic.apps.agents.error import AgentError
from logic.apps.agents.model import Agent
from logic.apps.jobs import service as work_service
from logic.apps.jobs.model import Job, Status
from logic.apps.modules import service as module_service
from logic.apps.modules.error import ModulesError
from logic.libs.exception.exception import AppException

apirouter = APIRouter(prefix='/api/v1/works', tags=['Jobs'])


@apirouter.route('/', methods=['POST'])
def exec(data: str):

    params_dict = {}
    if data:
        params_dict = yaml.load(
            data, Loader=yaml.FullLoader) if _is_yaml(data) else data

    _valid_params(params_dict)

    job = Job(
        name=params_dict['name'],
        module_name=params_dict['module_name'],
        module_repo=params_dict['module_repo'],
        agent_type=params_dict['agent_type'],
        params=params_dict['params']
    )

    id = work_service.add(job)

    return JSONResponse(id=id), 201


@apirouter.route('/<id>/logs', methods=['GET'])
def logs(id: str):

    result = work_service.get_logs(id)

    return result, 200


@apirouter.route('/<id>', methods=['DELETE'])
def delete(id: str):

    work_service.delete(id)
    return JSONResponse('', 200)


@apirouter.route('/', methods=['DELETE'])
def delete_by_filters(status: str = None):

    if status:
        work_service.delete_by_status(Status(status))

    return JSONResponse('', 200)


@apirouter.route('/<id>', methods=['GET'])
def get(id: str):

    result = work_service.get(id)
    if not result:
        return '', 204

    result_dict = {
        "id": result.id,
        "name": result.name,
        "module_repo": result.module_repo,
        "module_name": result.module_name,
        "params": result.params,
        "agent_type": result.agent_type,
        'agent': {
            "type": result.agent.type,
            "host": result.agent.host,
            "port": result.agent.port,
            "id": result.agent.id
        } if result.agent else "",
        "status": result.status.value,
        "start_date": result.start_date.isoformat() if result.start_date else "",
        "running_date": result.running_date.isoformat() if result.running_date else "",
        "terminated_date": result.terminated_date.isoformat() if result.terminated_date else ""
    }

    return JSONResponse(result_dict), 200


@apirouter.route('/<id>/finish', methods=['PATCH'])
def finish(id: str, body: Dict[str, object]):

    status = Status(body["status"])

    work_service.finish_work(id, status)
    return JSONResponse('', 200)


@apirouter.route('/<id>/status/<status>', methods=['PATCH'])
def changeStatus(id: str, status: str):

    work_service.change_status(id, Status(status))
    return JSONResponse('', 200)


@apirouter.route('/', methods=['GET'])
def list():

    result = work_service.list_all()
    return JSONResponse(result), 200


@apirouter.route('/status', methods=['GET'])
def get_status_works():
    return JSONResponse(work_service.list_types()), 200


@apirouter.route('/all/short', methods=['GET'])
def get_all_short():

    result = work_service.get_all_short()
    return JSONResponse(result), 200


@apirouter.route('/<id>/workspace', methods=['GET'])
def download_workspace(id: str):

    result = work_service.download_workspace(id)
    headers = {
        'Content-Disposition': f'attachment; filename="{id}.zip"'}

    return Response(
        open(result, 'rb').read(),
        media_type='application/octet-stream',
        headers=headers
    )


def _is_yaml(text: str) -> bool:
    try:
        yaml.load(text, Loader=yaml.FullLoader)
        return True

    except Exception:
        return False


@apirouter.route('/', methods=['PUT'])
def modify(data: Dict[str, object]):

    params_dict = {}
    if data:
        params_dict = yaml.load(data, Loader=yaml.FullLoader) if _is_yaml(
            data) else data

    _valid_params(params_dict)

    job = Job(
        id=params_dict['id'],
        name=params_dict['name'],
        module_name=params_dict['module_name'],
        module_repo=params_dict['module_repo'],
        agent_type=params_dict['agent_type'],
        params=params_dict['params'],
        status=Status(params_dict['status'])
    )

    if 'agent' in params_dict:
        job.agent = Agent(
            id=params_dict['agent']['id'],
            host=params_dict['agent']['host'],
            port=params_dict['agent']['port'],
            type=params_dict['agent']['type']
        )

    if 'running_date' in params_dict:
        job.running_date = datetime.fromisoformat(params_dict['running_date'])

    if 'terminated_date' in params_dict:
        job.terminated_date = datetime.fromisoformat(
            params_dict['terminated_date'])

    if 'start_date' in params_dict:
        job.start_date = datetime.fromisoformat(params_dict['start_date'])

    work_service.modify(job)

    return JSONResponse('', 200)


def _valid_params(params: Dict[str, object]):

    if not 'agent_type' in params:
        msj = f'El tipo de agente es requerido'
        raise AppException(AgentError.AGENT_PARAM_ERROR, msj)

    agent_type = params['agent_type']
    if not agent_service.get_by_type(agent_type):
        msj = f'No existen agentes activos de tipo {agent_type}'
        raise AppException(AgentError.AGENT_PARAM_ERROR, msj)

    if not 'module_name' in params or not 'module_repo' in params or not params['module_name'] in module_service.list_all(params['module_repo']):
        name = params['module_name']
        msj = f'No existe modulo de nombre {name}'
        raise AppException(ModulesError.MODULE_NO_EXIST_ERROR, msj)
