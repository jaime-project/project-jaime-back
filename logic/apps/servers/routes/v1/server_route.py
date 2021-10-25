from flask import Blueprint, jsonify, request
from logic.apps.servers.models.server_model import Server
from logic.apps.servers.services import server_service

blue_print = Blueprint('servers', __name__, url_prefix='/api/v1/servers')


@blue_print.route('/', methods=['POST'])
def post():
    s = request.json
    server_service.add(Server(
        name=s['name'],
        url=s['url'],
        token=s['token'],
        version=s['version']
    ))
    return '', 201


@blue_print.route('/<name>', methods=['GET'])
def get(name: str):
    s = server_service.get(name)
    return jsonify(s.__dict__), 200


@blue_print.route('/', methods=['GET'])
def list_all():

    return jsonify(server_service.list_all()), 200


@blue_print.route('/<name>', methods=['DELETE'])
def delete(name: str):
    server_service.delete(name)
    return '', 200
