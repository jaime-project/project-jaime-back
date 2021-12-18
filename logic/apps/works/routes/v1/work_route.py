import ntpath
from io import BytesIO

import yaml
from flask import Blueprint, jsonify, request, send_file
from logic.apps.works.models.work_model import Status
from logic.apps.works.services import work_service

blue_print = Blueprint('works', __name__, url_prefix='/api/v1/works')


@blue_print.route('/', methods=['POST'])
def exec():

    params_dict = yaml.load(request.data, Loader=yaml.FullLoader) if _is_yaml(
        request.data) else request.json

    id = work_service.start(params_dict)

    return jsonify(id=id), 201


@blue_print.route('/<id>/logs', methods=['GET'])
def logs(id: str):

    result = work_service.get_logs(id)

    return result, 200


@blue_print.route('/<id>', methods=['DELETE'])
def delete(id: str):

    work_service.delete(id)
    return '', 200


@blue_print.route('/<id>', methods=['GET'])
def get(id: str):

    result = work_service.get(id)
    if not result:
        return '', 204

    result_dict = {
        "id": result.id,
        "name": result.name,
        "module_name": result.module_name,
        "params": result.params,
        'agent': {
            "type": result.agent.type.value,
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

    work_service.finish_work(id)
    return '', 200


@blue_print.route('/', methods=['GET'])
def list():

    result = work_service.list_all()
    return jsonify(result), 200


@blue_print.route('/all/short', methods=['GET'])
def get_all_short():

    result = work_service.get_all_short()
    return jsonify(result), 200


@blue_print.route('/<id>/workspace', methods=['GET'])
def download_workspace(id: str):

    result = work_service.download_workspace(id)
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
