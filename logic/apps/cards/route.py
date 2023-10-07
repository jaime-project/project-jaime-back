from datetime import datetime

import yaml
from flask import Blueprint, jsonify, request

from logic.apps.cards import service
from logic.apps.cards.model import Card

blue_print = Blueprint('cards', __name__, url_prefix='/api/v1/cards')


@blue_print.route('/', methods=['POST'])
def add():

    params_dict = yaml.load(request.data, Loader=yaml.FullLoader) if _is_yaml(
        request.data) else request.json

    card = Card(
        name=params_dict['name'],
        description=params_dict['description'],
        job_module_repo=params_dict['job_module_repo'],
        job_module_name=params_dict['job_module_name'],
        job_agent_type=params_dict['job_agent_type'],
        job_default_docs=params_dict['job_default_docs'],
    )

    id = service.add(card)

    return jsonify(id=id), 201


def _is_yaml(text: str) -> bool:
    try:
        yaml.load(text, Loader=yaml.FullLoader)
        return True

    except Exception:
        return False


@blue_print.route('/<id>', methods=['DELETE'])
def delete(id: str):

    service.delete(id)
    return '', 200


@blue_print.route('/<id>', methods=['GET'])
def get(id: str):

    card = service.get(id)
    if not card:
        return '', 204

    result_dict = {
        'name': card.name,
        'description': card.description,
        'job_module_repo': card.job_module_repo,
        'job_module_name': card.job_module_name,
        'job_agent_type': card.job_agent_type,
        'id': card.id,
        'creation_date': card.creation_date.isoformat(),
    }

    return jsonify(result_dict), 200


@blue_print.route('/', methods=['GET'])
def list():

    result = service.list_all()
    return jsonify(result), 200


@blue_print.route('/all/short', methods=['GET'])
def get_all_short():

    filter = request.args.get('filter', None)

    result = service.get_all_short(filter)
    return jsonify(result), 200


@blue_print.route('/', methods=['PUT'])
def modify():

    params_dict = yaml.load(request.data, Loader=yaml.FullLoader) if _is_yaml(
        request.data) else request.json

    card = Card(
        name=params_dict['name'],
        description=params_dict['description'],
        job_module_repo=params_dict['job_module_repo'],
        job_module_name=params_dict['job_module_name'],
        job_agent_type=params_dict['job_agent_type'],
        creation_date=params_dict['creation_date'],
        id=params_dict['id']
    )

    service.modify(card)

    return '', 200


@blue_print.route('/<id>/run', methods=['POST'])
def run(id: str):

    params_dict = yaml.load(request.data, Loader=yaml.FullLoader) if _is_yaml(
        request.data) else request.json

    id = service.run(id, params_dict)

    return jsonify(id=id), 200


@blue_print.route('/<id>/docs', methods=['POST'])
def postDocs(id: str):

    docs = request.data

    service.post_docs(id, docs)

    return '', 201


@blue_print.route('/<id>/docs', methods=['PUT'])
def putDocs(id: str):

    docs = request.data

    service.post_docs(id, docs)

    return '', 201


@blue_print.route('/<id>/docs', methods=['GET'])
def getDocs(id: str):

    docs = service.get_docs(id)

    return docs, 201
