import yaml
from flask import Blueprint, jsonify, request
from logic.apps.agents.models.agent_model import Agent
from logic.apps.agents.services import agent_service
from logic.apps.servers.models.server_model import ServerType

blue_print = Blueprint('agent', __name__, url_prefix='/api/v1/agents')


@blue_print.route('/', methods=['POST'])
def post():
    j = request.json
    n = Agent(
        id=j['id'],
        host=j['host'],
        port=j['port'],
        type=ServerType(j['type'])
    )

    agent_service.add(n)

    return jsonify(id=n.id), 201


@blue_print.route('/<id>', methods=['DELETE'])
def delete(id: str):

    agent_service.delete(id)
    return '', 200


@blue_print.route('/', methods=['GET'])
def list_all():

    result = agent_service.list_all()
    return jsonify(result), 200


@blue_print.route('/all/short', methods=['GET'])
def get_all_short():

    result = agent_service.get_all_short()
    return jsonify(result), 200


@blue_print.route('/<id>', methods=['GET'])
def get(id: str):

    n = agent_service.get(id)
    if not n:
        return '', 204

    result = {
        "type": n.type.value,
        "host": n.host,
        "port": n.port,
        "id": n.id,
    }

    return jsonify(result), 200
