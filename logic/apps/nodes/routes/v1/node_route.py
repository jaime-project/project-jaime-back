import yaml
from flask import Blueprint, jsonify, request
from logic.apps.nodes.models.node_model import Node
from logic.apps.nodes.services import node_service

blue_print = Blueprint('nodes', __name__, url_prefix='/api/v1/nodes')


@blue_print.route('/', methods=['POST'])
def exec():
    j = request.json
    n = Node(
        host=j['host'],
        port=j['port'],
        type=j['type']
    )

    node_service.add(n)

    return jsonify(id=n.id), 201


@blue_print.route('/<id>', methods=['DELETE'])
def delete(id: str):

    work_service.delete(id)
    return '', 200


@blue_print.route('/', methods=['GET'])
def get():

    result = work_service.list_all_running()
    return jsonify(result), 200


def _is_yaml(text: str) -> bool:
    try:
        yaml.load(request.data, Loader=yaml.FullLoader)
        return True

    except Exception:
        return False
