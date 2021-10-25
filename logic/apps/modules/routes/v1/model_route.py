from flask import Blueprint, Response, jsonify, request
from logic.apps.modules.services import module_service

blue_print = Blueprint('modules', __name__, url_prefix='/api/v1/modules')


@blue_print.route('/<name>', methods=['POST'])
def post(name: str):
    content = request.get_data().decode('utf8')
    module_service.add(name, content)
    return '', 201


@blue_print.route('/<name>', methods=['GET'])
def get(name: str):
    content = module_service.get(name)
    return Response(content, mimetype='text/plain', status=201)


@blue_print.route('/', methods=['GET'])
def list_all():
    return jsonify(module_service.list_all()), 200


@blue_print.route('/<name>', methods=['DELETE'])
def delete(name: str):
    module_service.delete(name)
    return '', 200
