from os import name
from flask import Blueprint, jsonify, request
from logic.apps.servers.models.server_model import Server, ServerType
from logic.apps.servers.services import server_service

blue_print = Blueprint('servers', __name__, url_prefix='/api/v1/servers')


@blue_print.route('/', methods=['POST'])
def post():
    s = request.json
    server_service.add(Server(
        name=s['name'],
        url=s['url'],
        token=s['token'],
        version=s['version'],
        type=ServerType(s['type'])
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


@blue_print.route('/types', methods=['GET'])
def list_types():
    return jsonify(server_service.list_types()), 200


@blue_print.route('/all/short', methods=['GET'])
def get_all_short():
    return jsonify(server_service.get_all_short()), 200


@blue_print.route('/<name>/test', methods=['GET'])
def test_server(name):
    return jsonify(server_service.test_server(name)), 200
