import ntpath
from datetime import datetime
from io import BytesIO

import yaml
from flask import Blueprint, jsonify, request, send_file

from logic.apps.clusters import service
from logic.apps.clusters.model import Cluster

blue_print = Blueprint('clusters', __name__, url_prefix='/api/v1/clusters')


@blue_print.route('/', methods=['POST'])
def post():
    s = request.json
    service.add(Cluster(
        name=s['name'],
        url=s['url'],
        token=s['token'],
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


@blue_print.route('/<name>/test/agent/<agent_type>', methods=['GET'])
def test_cluster(name: str, agent_type: str):
    return jsonify(service.test_cluster(name, agent_type)), 200


@blue_print.route('/<name>', methods=['PUT'])
def modify_cluster(name):

    s = request.json
    server = Cluster(
        name=s['name'],
        url=s['url'],
        token=s['token'],
    )
    service.modify(name, server)

    return '', 200


@blue_print.route('/<name>/yamls', methods=['GET'])
def export_cluster(name: str):

    dict_objects = service.export_cluster(name)
    dict_yaml = str(yaml.dump(dict_objects))

    name_yaml = datetime.now().isoformat() + '.yaml'

    return send_file(BytesIO(dict_yaml.encode()),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     download_name=ntpath.basename(name_yaml))
