from flask import Blueprint, jsonify, request

from logic.apps.login import service
from logic.apps.login.dto import to_login
from logic.libs.exception.exception import AppException

blue_print = Blueprint('login', __name__, url_prefix='/api/v1/login')


@blue_print.route('/', methods=['POST'])
def login():

    login = to_login(request.json)
    try:
        token = service.login(login)
        return token, 200

    except AppException as app:
        return jsonify(app.to_json()), 403


@blue_print.route('/refresh', methods=['GET'])
def refresh():
    return '', 200
