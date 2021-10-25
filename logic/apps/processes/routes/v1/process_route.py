import yaml
from flask import Blueprint, jsonify, request
from logic.apps.works.services import exec_work_service

blue_print = Blueprint('works', __name__, url_prefix='/api/v1/works')


@blue_print.route('/', methods=['POST'])
def exec():

    id = exec_work_service.exec(request.json)

    return jsonify(id=id), 200


@blue_print.route('/yaml', methods=['POST'])
def exec_yaml():

    params = yaml.load(request.data, Loader=yaml.FullLoader)
    id = exec_work_service.exec(params)

    return jsonify(id=id), 200
