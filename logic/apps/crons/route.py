from datetime import datetime
from typing import Dict

import yaml
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from logic.apps.crons import runner, service
from logic.apps.crons.model import CronStatus, CronWork

apirouter = APIRouter(prefix='/api/v1/crons', tags=['Crons'])


@apirouter.route('/', methods=['POST'])
def add(data: Dict[str, object]):

    params_dict = yaml.load(
        data, Loader=yaml.FullLoader) if _is_yaml(data) else data

    cron = CronWork(
        name=params_dict['name'],
        cron_expression=params_dict['cron_expression'],
        work_module_repo=params_dict['work_module_repo'],
        work_module_name=params_dict['work_module_name'],
        work_agent_type=params_dict['work_agent_type'],
        work_params=params_dict['work_params'] if params_dict['work_params'] else {
        }
    )

    id = service.add(cron)

    return JSONResponse(id=id), 201


def _is_yaml(text: str) -> bool:
    try:
        yaml.load(text, Loader=yaml.FullLoader)
        return True

    except Exception:
        return False


@apirouter.route('/<id>', methods=['DELETE'])
def delete(id: str):

    service.delete(id)
    return JSONResponse('', 200)


@apirouter.route('/', methods=['DELETE'])
def delete_by_filters(status: str = None):

    if status:
        service.delete_by_status(CronStatus(status))

    return JSONResponse('', 200)


@apirouter.route('/<id>', methods=['GET'])
def get(id: str):

    cron = service.get(id)
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
        'work_params': cron.work_params
    }

    return JSONResponse(result_dict), 200


@apirouter.route('/<id>/status/<status>', methods=['PATCH'])
def change_status(id: str, status: str):

    if CronStatus(status) == CronStatus.ACTIVE:
        runner.activate_cron(id)
    else:
        runner.desactivate_cron(id)

    return JSONResponse('', 200)


@apirouter.route('/', methods=['GET'])
def list():

    result = service.list_all()
    return JSONResponse(result), 200


@apirouter.route('/status', methods=['GET'])
def get_status_crons():

    return JSONResponse(service.list_status()), 200


@apirouter.route('/all/short', methods=['GET'])
def get_all_short():

    result = service.get_all_short()
    return JSONResponse(result), 200


@apirouter.route('/', methods=['PUT'])
def modify(data: Dict[str, object]):

    params_dict = yaml.load(
        data, Loader=yaml.FullLoader) if _is_yaml(data) else data

    cron = CronWork(
        name=params_dict['name'],
        cron_expression=params_dict['cron_expression'],
        work_module_repo=params_dict['work_module_repo'],
        work_module_name=params_dict['work_module_name'],
        work_agent_type=params_dict['work_agent_type'],
        work_params=params_dict['work_params'],
        creation_date=datetime.fromisoformat(params_dict['creation_date']),
        status=CronStatus(params_dict['status']),
        id=params_dict['id']
    )

    service.modify(cron)

    return JSONResponse('', 200)
