from flask import Blueprint, jsonify, request
from logic.apps.configs.services import config_service

blue_print = Blueprint('configs', __name__, url_prefix='/api/v1/configs')


@blue_print.route('/requirements', methods=['GET'])
def get():
    return config_service.getRequirements(), 200


@blue_print.route('/requirements', methods=['POST'])
def post():
    config_service.updateRequirements(request.data.decode())
    return '', 200
