from datetime import datetime

import yaml
from flask import Blueprint, jsonify, request

from logic.apps.crons import runner, service
from logic.apps.crons.model import CronStatus, CronWork

blue_print = Blueprint('crons', __name__, url_prefix='/api/v1/crons')


@blue_print.route('/', methods=['POST'])
def add():

    params_dict = yaml.load(request.data, Loader=yaml.FullLoader) if _is_yaml(
        request.data) else request.json

    cron = CronWork(
        name=params_dict['name'],
        cron_expression=params_dict['cron_expression'],
        job_module_repo=params_dict['job_module_repo'],
        job_module_name=params_dict['job_module_name'],
        job_agent_type=params_dict['job_agent_type'],
        job_params=params_dict['job_params'] if params_dict['job_params'] else {
        }
    )

    id = service.add(cron)

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
        service.delete_by_status(CronStatus(status))

    return '', 200


@blue_print.route('/<id>', methods=['GET'])
def get(id: str):

    cron = service.get(id)
    if not cron:
        return '', 204

    result_dict = {
        'name': cron.name,
        'cron_expression': cron.cron_expression,
        'job_module_repo': cron.job_module_repo,
        'job_module_name': cron.job_module_name,
        'job_agent_type': cron.job_agent_type,
        'id': cron.id,
        'creation_date': cron.creation_date.isoformat(),
        'status': cron.status.value,
        'job_params': cron.job_params
    }

    return jsonify(result_dict), 200


@blue_print.route('/<id>/status/<status>', methods=['PATCH'])
def change_status(id: str, status: str):

    if CronStatus(status) == CronStatus.ACTIVE:
        runner.activate_cron(id)
    else:
        runner.desactivate_cron(id)

    return '', 200


@blue_print.route('/', methods=['GET'])
def list():

    result = service.list_all()
    return jsonify(result), 200


@blue_print.route('/status', methods=['GET'])
def get_status_crons():

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

    cron = CronWork(
        name=params_dict['name'],
        cron_expression=params_dict['cron_expression'],
        job_module_repo=params_dict['job_module_repo'],
        job_module_name=params_dict['job_module_name'],
        job_agent_type=params_dict['job_agent_type'],
        job_params=params_dict['job_params'],
        creation_date=datetime.fromisoformat(params_dict['creation_date']),
        status=CronStatus(params_dict['status']),
        id=params_dict['id']
    )

    service.modify(cron)

    return '', 200
