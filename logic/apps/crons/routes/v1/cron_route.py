import json
from datetime import datetime

import yaml
from flask import Blueprint, jsonify, request
from logic.apps.crons.models.cron_model import CronStatus, CronWork
from logic.apps.crons.services import cron_service

from ...models.cron_model import CronWork

blue_print = Blueprint('crons', __name__, url_prefix='/api/v1/crons')


@blue_print.route('/', methods=['POST'])
def add():

    params_dict = yaml.load(request.data, Loader=yaml.FullLoader) if _is_yaml(
        request.data) else request.json

    cron = CronWork(
        name=params_dict['name'],
        cron_expression=params_dict['cron_expression'],
        cron_module_repo=params_dict['cron_module_repo'],
        cron_module_name=params_dict['cron_module_name'],
        cron_agent_type=params_dict['cron_agent_type'],
        cron_params=params_dict['params']
    )

    id = cron_service.add(cron)

    return jsonify(id=id), 201


def _is_yaml(text: str) -> bool:
    try:
        yaml.load(text, Loader=yaml.FullLoader)
        return True

    except Exception:
        return False


@blue_print.route('/<id>', methods=['DELETE'])
def delete(id: str):

    cron_service.delete(id)
    return '', 200


@blue_print.route('/<id>', methods=['GET'])
def get(id: str):

    cron = cron_service.get(id)
    if not cron:
        return '', 204

    result_dict = {
        'name': cron.name,
        'cron_expression': cron.cron_expression,
        'work_module_repo': cron.work_module_repo,
        'work_module_name': cron.work_module_name,
        'work_agent_type': cron.work_agent_type,
        'id': cron.id,
        'creation_date': cron.creation_date.isoformat(),
        'status': cron.status.value,
        'work_params': json.dumps(cron.work_params)
    }

    return jsonify(result_dict), 200


@blue_print.route('/<id>/status/<status>', methods=['PATCH'])
def change_status(id: str, status: str):

    cron_service.change_status(id, CronStatus(status))
    return '', 200


@blue_print.route('/', methods=['GET'])
def list():

    result = cron_service.list_all()
    return jsonify(result), 200


@blue_print.route('/status', methods=['GET'])
def get_status_crons():
    return jsonify(cron_service.list_status()), 200


@blue_print.route('/all/short', methods=['GET'])
def get_all_short():

    result = cron_service.get_all_short()
    return jsonify(result), 200


@blue_print.route('/', methods=['PUT'])
def modify():

    params_dict = yaml.load(request.data, Loader=yaml.FullLoader) if _is_yaml(
        request.data) else request.json

    cron = CronWork(
        name=params_dict['name'],
        cron_expression=params_dict['cron_expression'],
        cron_module_repo=params_dict['cron_module_repo'],
        cron_module_name=params_dict['cron_module_name'],
        cron_agent_type=params_dict['cron_agent_type'],
        cron_params=params_dict['params'],
        creation_date=datetime.fromisoformat(params_dict['creation_date']),
        status=CronStatus(params_dict['status']),
        id=params_dict['id']
    )

    cron_service.modify(cron)

    return '', 200
