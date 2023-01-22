import yaml
from flask import Blueprint, Response, jsonify, request
from logic.apps.docs import service

blue_print = Blueprint(
    'docs', __name__, url_prefix='/api/v1/repos/<repo>/docs')


@blue_print.route('/<name>', methods=['POST'])
def post(name: str, repo: str):
    content = request.get_data().decode('utf8')
    service.add(name, content, repo)
    return '', 201


@blue_print.route('/<name>', methods=['GET'])
def get(name: str, repo: str):
    content = service.get(name, repo)
    return Response(content, mimetype='text/plain', status=200)


@blue_print.route('/<name>/yaml', methods=['GET'])
def get_yaml(name: str, repo: str):
    content = service.get(name, repo)

    dict_yaml = yaml.load(content)
    if 'yaml' in dict_yaml:
        dict_yaml = dict_yaml['yaml']
        return Response(yaml.dump(dict_yaml), mimetype='text/plain', status=200)

    return Response('', mimetype='text/plain', status=200)


@blue_print.route('/', methods=['GET'])
def list_all(repo: str):
    return jsonify(service.list_all(repo)), 200


@blue_print.route('/<name>', methods=['DELETE'])
def delete(name: str, repo: str):
    service.delete(name, repo)
    return '', 200


@blue_print.route('/<name>', methods=['PUT'])
def modify(name: str, repo: str):
    content = request.get_data().decode('utf8')
    service.modify(name, content, repo)
    return '', 200
