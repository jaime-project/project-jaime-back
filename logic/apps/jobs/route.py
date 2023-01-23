import ntpath
from datetime import datetime
from io import BytesIO
from typing import Dict

import yaml
from flask import Blueprint, jsonify, request, send_file

from logic.apps.agents import service as agent_service
from logic.apps.agents.error import AgentError
from logic.apps.agents.model import Agent
from logic.apps.jobs import service
from logic.apps.jobs.model import Job, Status
from logic.apps.modules import service as module_service
from logic.apps.modules.error import ModulesError
from logic.libs.exception.exception import AppException

blue_print = Blueprint('jobs', __name__, url_prefix='/api/v1/jobs')


@blue_print.route('/', methods=['POST'])
def exec():

    params_dict = {}
    if request.data:
        params_dict = yaml.load(request.data, Loader=yaml.FullLoader) if _is_yaml(
            request.data) else request.json

    _valid_params(params_dict)

    work = Job(
        name=params_dict['name'],
        module_name=params_dict['module_name'],
        module_repo=params_dict['module_repo'],
        agent_type=params_dict['agent_type'],
        params=params_dict['params']
    )

    id = service.add(work)

    return jsonify(id=id), 201


@blue_print.route('/<id>/logs', methods=['GET'])
def logs(id: str):

    result = service.get_logs(id)

    return result, 200


@blue_print.route('/<id>', methods=['DELETE'])
def delete(id: str):

    service.delete(id)
    return '', 200


@blue_print.route('/', methods=['DELETE'])
def delete_by_filters():

    status = request.args.get('status', None)
    if status:
        service.delete_by_status(Status(status))

    return '', 200


@blue_print.route('/<id>', methods=['GET'])
def get(id: str):

    result = service.get(id)
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

    return jsonify(result_dict), 200


@blue_print.route('/<id>/finish', methods=['PATCH'])
def finish(id: str):

    body = request.json
    status = Status(body["status"])

    service.finish_work(id, status)
    return '', 200


@blue_print.route('/<id>/status/<status>', methods=['PATCH'])
def changeStatus(id: str, status: str):

    service.change_status(id, Status(status))
    return '', 200


@blue_print.route('/', methods=['GET'])
def list():

    result = service.list_all()
    return jsonify(result), 200


@blue_print.route('/status', methods=['GET'])
def get_status_works():
    return jsonify(service.list_types()), 200


@blue_print.route('/all/short', methods=['GET'])
def get_all_short():

    size = int(request.args.get('size', 3))
    page = int(request.args.get('page', 1))
    filter = request.args.get('filter', None)
    order = request.args.get('order', None)

    return jsonify(service.get_all_short(size, page, filter, order)), 200


@blue_print.route('/<id>/workspace', methods=['GET'])
def download_workspace(id: str):

    result = service.download_workspace(id)
    return send_file(BytesIO(result),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=ntpath.basename(f'{id}.zip'))


def _is_yaml(text: str) -> bool:
    try:
        yaml.load(text, Loader=yaml.FullLoader)
        return True

    except Exception:
        return False


@blue_print.route('/', methods=['PUT'])
def modify():

    params_dict = {}
    if request.data:
        params_dict = yaml.load(request.data, Loader=yaml.FullLoader) if _is_yaml(
            request.data) else request.json

    _valid_params(params_dict)

    work = Job(
        id=params_dict['id'],
        name=params_dict['name'],
        module_name=params_dict['module_name'],
        module_repo=params_dict['module_repo'],
        agent_type=params_dict['agent_type'],
        params=params_dict['params'],
        status=Status(params_dict['status'])
    )

    if 'agent' in params_dict:
        work.agent = Agent(
            id=params_dict['agent']['id'],
            host=params_dict['agent']['host'],
            port=params_dict['agent']['port'],
            type=params_dict['agent']['type']
        )

    if 'running_date' in params_dict:
        work.running_date = datetime.fromisoformat(params_dict['running_date'])

    if 'terminated_date' in params_dict:
        work.terminated_date = datetime.fromisoformat(
            params_dict['terminated_date'])

    if 'start_date' in params_dict:
        work.start_date = datetime.fromisoformat(params_dict['start_date'])

    service.modify(work)

    return '', 200


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
