import ntpath
from datetime import datetime
from io import BytesIO

import yaml
from flask import Blueprint, jsonify, request, send_file

from logic.apps.servers.models.server_model import Server
from logic.apps.servers.services import server_service

blue_print = Blueprint('servers', __name__, url_prefix='/api/v1/servers')


@blue_print.route('/', methods=['POST'])
def post():
    s = request.json
    server_service.add(
        Server(
            name=s['name'],
            host=s['host'],
            port=s['port'],
            user=s['user'],
            password=s['password']
        ))
    return '', 201


@blue_print.route('/<name>', methods=['GET'])
def get(name: str):
    s = server_service.get(name)
    if not s:
        return '', 204

    return jsonify(s.__dict__()), 200


@blue_print.route('/', methods=['GET'])
def list_all():
    return jsonify(server_service.list_all()), 200


@blue_print.route('/<name>', methods=['DELETE'])
def delete(name: str):
    server_service.delete(name)
    return '', 200


@blue_print.route('/all/short', methods=['GET'])
def get_all_short():
    return jsonify(server_service.get_all_short()), 200


@blue_print.route('/<name>/test', methods=['GET'])
def test_server(name):
    return jsonify(server_service.test_server(name)), 200


@blue_print.route('/<name>', methods=['PUT'])
def put(name):

    s = request.json
    server = Server(
        name=s['name'],
        host=s['host'],
        port=s['port'],
        user=s['user'],
        password=s['password']
    )
    server_service.modify(name, server)

    return '', 200


@blue_print.route('/<name>/yamls', methods=['GET'])
def export_server(name: str):

    dict_objects = server_service.export_server(name)
    dict_yaml = str(yaml.dump(dict_objects))

    name_yaml = datetime.now().isoformat() + '.yaml'

    return send_file(BytesIO(dict_yaml.encode()),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=ntpath.basename(name_yaml))
