import ntpath
from datetime import datetime
from io import BytesIO

import yaml
from flask import Blueprint, jsonify, request, send_file

from logic.apps.clusters.models.cluster_model import Cluster
from logic.apps.clusters.services import cluster_service

blue_print = Blueprint('clusters', __name__, url_prefix='/api/v1/clusters')


@blue_print.route('/', methods=['POST'])
def post():
    s = request.json
    cluster_service.add(Cluster(
        name=s['name'],
        url=s['url'],
        token=s['token'],
        version=s['version'],
        type=s['type']
    ))
    return '', 201


@blue_print.route('/<name>', methods=['GET'])
def get(name: str):
    s = cluster_service.get(name)
    if not s:
        return '', 204

    return jsonify(s.__dict__()), 200


@blue_print.route('/', methods=['GET'])
def list_all():

    return jsonify(cluster_service.list_all()), 200


@blue_print.route('/<name>', methods=['DELETE'])
def delete(name: str):
    cluster_service.delete(name)
    return '', 200


@blue_print.route('/all/short', methods=['GET'])
def get_all_short():
    return jsonify(cluster_service.get_all_short()), 200


@blue_print.route('/<name>/test', methods=['GET'])
def test_cluster(name):
    return jsonify(cluster_service.test_cluster(name)), 200


@blue_print.route('/<name>', methods=['PUT'])
def modify_server(name):

    s = request.json
    server = Cluster(
        name=s['name'],
        url=s['url'],
        token=s['token'],
        version=s['version'],
        type=s['type']
    )
    cluster_service.modify(name, server)

    return '', 200


@blue_print.route('/<name>/yamls', methods=['GET'])
def export_cluster(name: str):

    dict_objects = cluster_service.export_cluster(name)
    dict_yaml = str(yaml.dump(dict_objects))

    name_yaml = datetime.now().isoformat() + '.yaml'

    return send_file(BytesIO(dict_yaml.encode()),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     attachment_filename=ntpath.basename(name_yaml))
