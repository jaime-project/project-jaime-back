from datetime import datetime

import yaml
from flask import Blueprint, jsonify, request

from logic.apps.hooks import service
from logic.apps.hooks.model import HookJob, HookStatus

blue_print = Blueprint('hooks', __name__, url_prefix='/api/v1/hooks')


@blue_print.route('/', methods=['POST'])
def add():

    params_dict = yaml.load(request.data, Loader=yaml.FullLoader) if _is_yaml(
        request.data) else request.json

    hook = HookJob(
        name=params_dict['name'],
        job_module_repo=params_dict['job_module_repo'],
        job_module_name=params_dict['job_module_name'],
        job_agent_type=params_dict['job_agent_type'],
        job_params=params_dict['job_params'] if params_dict['job_params'] else {
        }
    )

    id = service.add(hook)

    return jsonify(id=id), 201


def _is_yaml(text: str) -> bool:
    try:
        yaml.load(text, Loader=yaml.FullLoader)
        return True

    except Exception:
        return False


@blue_print.route('/<id>', methods=['DELETE'])
def delete(id: str):

    service.delete(id)
    return '', 200


@blue_print.route('/', methods=['DELETE'])
def delete_by_filters():

    status = request.args.get('status', None)
    if status:
        service.delete_by_status(HookStatus(status))

    return '', 200


@blue_print.route('/<id>', methods=['GET'])
def get(id: str):

    hook = service.get(id)
    if not hook:
        return '', 204

    result_dict = {
        'name': hook.name,
        'job_module_repo': hook.job_module_repo,
        'job_module_name': hook.job_module_name,
        'job_agent_type': hook.job_agent_type,
        'id': hook.id,
        'creation_date': hook.creation_date.isoformat(),
        'status': hook.status.value,
        'job_params': hook.job_params
    }

    return jsonify(result_dict), 200


@blue_print.route('/', methods=['GET'])
def list():

    result = service.list_all()
    return jsonify(result), 200


@blue_print.route('/status', methods=['GET'])
def get_status_hooks():

    return jsonify(service.list_status()), 200


@blue_print.route('/all/short', methods=['GET'])
def get_all_short():

    size = int(request.args.get('size', 10))
    page = int(request.args.get('page', 1))
    filter = request.args.get('filter', None)
    order = request.args.get('order', None)

    result = service.get_all_short(size, page, filter, order)
    return jsonify(result), 200


@blue_print.route('/', methods=['PUT'])
def modify():

    params_dict = yaml.load(request.data, Loader=yaml.FullLoader) if _is_yaml(
        request.data) else request.json

    hook = HookJob(
        name=params_dict['name'],
        job_module_repo=params_dict['job_module_repo'],
        job_module_name=params_dict['job_module_name'],
        job_agent_type=params_dict['job_agent_type'],
        job_params=params_dict['job_params'],
        creation_date=datetime.fromisoformat(params_dict['creation_date']),
        status=HookStatus(params_dict['status']),
        id=params_dict['id']
    )

    service.modify(hook)

    return '', 200


@blue_print.route('/exec/<id>', methods=['GET'])
def exec(id: str):

    hook = service.get(id)

    id = service.exec(hook)

    return jsonify(id=id), 201


@blue_print.route('/<id>/status/<status>', methods=['PATCH'])
def change_status(id: str, status: str):

    if HookStatus(status) == HookStatus.ACTIVE:
        service.activate_cron(id)
    else:
        service.desactivate_cron(id)

    return '', 200
