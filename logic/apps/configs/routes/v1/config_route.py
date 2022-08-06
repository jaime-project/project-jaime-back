import yaml
from flask import Blueprint, jsonify, request
from logic.apps.configs.services import config_service

blue_print = Blueprint('configs', __name__, url_prefix='/api/v1/configs')


@blue_print.route('/requirements', methods=['GET'])
def get():
    return config_service.get_requirements(), 200


@blue_print.route('/requirements', methods=['POST'])
def post():
    config_service.update_requirements(request.data.decode())
    return '', 200


@blue_print.route('/objects', methods=['POST'])
def post_objects():

    dict_yaml = yaml.load(request.data, Loader=yaml.FullLoader)
    replace = request.args.get('replace', False)

    config_service.update_objects(dict_yaml, replace)

    return '', 200
