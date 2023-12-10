import ntpath
from datetime import datetime
from io import BytesIO

import yaml
from flask import Blueprint, jsonify, request, send_file

from logic.apps.libraries import service
from logic.apps.libraries.model import Library

blue_print = Blueprint('libraries', __name__, url_prefix='/api/v1/libraries')


@blue_print.route('/', methods=['POST'])
def post():
    s = request.json
    service.add(
        Library(
            name=s['name'],
            description=s['host'],
            repo=s['repo'],
            path=s['path'],
            branch=s['branch'],
            user=s['user'],
            password=s['password']
        ))
    return '', 201


@blue_print.route('/<name>', methods=['GET'])
def get(name: str):
    s = service.get(name)
    if not s:
        return '', 204

    return jsonify(s.__dict__()), 200


@blue_print.route('/', methods=['GET'])
def list_all():
    return jsonify(service.list_all()), 200


@blue_print.route('/<name>', methods=['DELETE'])
def delete(name: str):
    service.delete(name)
    return '', 200


@blue_print.route('/all/short', methods=['GET'])
def get_all_short():

    size = int(request.args.get('size', 3))
    page = int(request.args.get('page', 1))
    filter = request.args.get('filter', None)
    order = request.args.get('order', None)

    return jsonify(service.get_all_short(size, page, filter, order)), 200


@blue_print.route('/<name>', methods=['PUT'])
def put(name):

    s = request.json
    server = Library(
        name=s['name'],
        description=s['host'],
        repo=s['repo'],
        path=s['path'],
        branch=s['branch'],
        user=s['user'],
        password=s['password']
    )
    service.modify(name, server)

    return '', 200


@blue_print.route('/<name>/reload', methods=['POST'])
def reload(name: str):
    service.load_library(name)
    return '', 200
