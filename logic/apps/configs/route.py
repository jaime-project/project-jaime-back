import json
from datetime import datetime
from typing import Dict

import yaml
from fastapi import APIRouter
from starlette.responses import Response

from logic.apps.configs import service

apirouter = APIRouter(prefix='/api/v1/configs', tags=['Configs'])


@apirouter.route('/requirements', methods=['GET'])
def get():
    return service.get_requirements(), 200


@apirouter.route('/requirements', methods=['POST'])
def post(data: bytes):
    service.update_requirements(data.decode())
    return '', 200


@apirouter.route('/yamls', methods=['POST'])
def post_yamls(data: Dict[str, object], replace: bool = False):

    dict_yaml = yaml.load(data, Loader=yaml.FullLoader)

    service.update_objects(dict_yaml, replace)

    return '', 200


@apirouter.route('/yamls/file', methods=['GET'])
def get_yamls():

    dict_objects = service.get_all_objects()
    dict_yaml = str(yaml.dump(dict_objects))

    name_yaml = datetime.now().isoformat() + '.yaml'
    headers = {
        'Content-Disposition': f'attachment; filename="{name_yaml}"'}

    return Response(
        open(dict_yaml, 'rb').read(),
        media_type='application/octet-stream',
        headers=headers
    )


@apirouter.route('/logs/jaime', methods=['GET'])
def get_jaime_logs():
    return service.get_jaime_logs(), 200


@apirouter.route('/logs/agents/<agent_id>', methods=['GET'])
def get_agent_logs(agent_id: str):
    return service.get_agent_logs(agent_id), 200


@apirouter.get('/vars')
def get_configs_vars():
    return json.dumps(service.get_configs_vars()), 200


@apirouter.route('/vars', methods=['PUT'])
def update_configs_vars(dict: Dict[str, object]):

    service.update_configs_vars(dict)

    return '', 200
