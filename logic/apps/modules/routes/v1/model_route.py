from flask import Blueprint, Response, jsonify, request
from logic.apps.modules.services import module_service

blue_print = Blueprint('modules', __name__,
                       url_prefix='/api/v1/repos/<repo>/modules')


@blue_print.route('/<name>', methods=['POST'])
def post(name: str, repo: str):
    content = request.get_data().decode('utf8')
    module_service.add(name, content, repo)
    return '', 201


@blue_print.route('/<name>', methods=['GET'])
def get(name: str, repo: str):
    content = module_service.get(name, repo)
    return Response(content, mimetype='text/plain', status=200)


@blue_print.route('/', methods=['GET'])
def list_all(repo: str):
    return jsonify(module_service.list_all(repo)), 200


@blue_print.route('/<name>', methods=['DELETE'])
def delete(name: str, repo: str):
    module_service.delete(name, repo)
    return '', 200


@blue_print.route('/<name>', methods=['PUT'])
def modify(name: str, repo: str):
    content = request.get_data().decode('utf8')
    module_service.modify(name, content, repo)
    return '', 200
