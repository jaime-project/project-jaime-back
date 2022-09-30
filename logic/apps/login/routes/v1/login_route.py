import yaml
from flask import Blueprint, jsonify, request
from logic.apps.agents.models.agent_model import Agent
from logic.apps.login.services import login_service
from logic.libs.exception.exception import AppException

blue_print = Blueprint('login', __name__, url_prefix='/api/v1/login')


@blue_print.route('/', methods=['POST'])
def login():
    j = request.json

    try:
        token = login_service.login(j['user'], j['pass'])
        return token, 200

    except AppException as app:
        return jsonify(app.to_json()), 403
