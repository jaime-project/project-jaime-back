from flask import Blueprint, jsonify, request

from logic.apps.agents import service
from logic.apps.agents.model import Agent
from logic.apps.login import service as login_service

blue_print = Blueprint('agent', __name__, url_prefix='/api/v1/agents')


@blue_print.route('/', methods=['POST'])
def post():
    j = request.json
    n = Agent(
        id=j['id'],
        host=j['host'],
        port=j['port'],
        type=j['type']
    )

    service.add(n)
    token = login_service.get_token()

    return token, 201


@blue_print.route('/<id>', methods=['DELETE'])
def delete(id: str):

    service.delete(id)
    return '', 200


@blue_print.route('/', methods=['GET'])
def list_all():

    agents = service.list_all()
    result = [
        {
            'id': a.id,
            'host': a.host,
            'port': a.port,
            'type': a.type,
            'status': a.status.value,
        }
        for a in agents
    ]

    return jsonify(result), 200


@blue_print.route('/all/short', methods=['GET'])
def get_all_short():

    size = int(request.args.get('size', 3))
    page = int(request.args.get('page', 1))
    filter = request.args.get('filter', None)
    order = request.args.get('order', None)

    return jsonify(service.get_all_short(size, page, filter, order)), 200


@blue_print.route('/<id>', methods=['GET'])
def get(id: str):

    n = service.get(id)
    if not n:
        return '', 204

    result = {
        "type": n.type,
        "host": n.host,
        "port": n.port,
        "id": n.id,
        'status': n.status.value,
    }

    return jsonify(result), 200


@blue_print.route('/types', methods=['GET'])
def list_types():
    return jsonify(service.list_types()), 200
