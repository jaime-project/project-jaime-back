from flask import Blueprint, Response, jsonify, request
from logic.apps.docs.services import doc_service

blue_print = Blueprint('docs', __name__, url_prefix='/api/v1/docs')


@blue_print.route('/<name>', methods=['POST'])
def post(name: str):
    content = request.get_data().decode('utf8')
    doc_service.add(name, content)
    return '', 201


@blue_print.route('/<name>', methods=['GET'])
def get(name: str):
    content = doc_service.get(name)
    return Response(content, mimetype='text/plain', status=200)


@blue_print.route('/', methods=['GET'])
def list_all():
    return jsonify(doc_service.list_all()), 200


@blue_print.route('/<name>', methods=['DELETE'])
def delete(name: str):
    doc_service.delete(name)
    return '', 200


@blue_print.route('/<name>', methods=['PUT'])
def modify(name: str):
    content = request.get_data().decode('utf8')
    doc_service.modify(name, content)
    return '', 200
