import ntpath
from datetime import datetime
from io import BytesIO

import yaml
from flask import Blueprint, request, send_file

from logic.apps.configs import service

blue_print = Blueprint('configs', __name__, url_prefix='/api/v1/configs')


@blue_print.route('/requirements', methods=['GET'])
def get():
    return service.get_requirements(), 200


@blue_print.route('/requirements', methods=['POST'])
def post():
    service.update_requirements(request.data.decode())
    return '', 200


@blue_print.route('/yamls', methods=['POST'])
def post_yamls():

    dict_yaml = yaml.load(request.data, Loader=yaml.FullLoader)
    replace = request.args.get('replace', False)

    service.update_objects(dict_yaml, replace)

    return '', 200


@blue_print.route('/yamls/file', methods=['GET'])
def get_yamls():

    dict_objects = service.get_all_objects()
    dict_yaml = str(yaml.dump(dict_objects))

    name_yaml = datetime.now().isoformat() + '.yaml'

    return send_file(BytesIO(dict_yaml.encode()),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=ntpath.basename(name_yaml))


@blue_print.route('/logs/jaime', methods=['GET'])
def get_jaime_logs():
    return service.get_jaime_logs(), 200


@blue_print.route('/logs/agents/<agent_id>', methods=['GET'])
def get_agent_logs(agent_id: str):
    return service.get_agent_logs(agent_id), 200
