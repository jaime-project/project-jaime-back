import ntpath
from datetime import datetime
from io import BytesIO
from typing import Any, Dict

import yaml
from flask import Blueprint, jsonify, request, send_file

from logic.apps.repos import service
from logic.apps.repos.model import Repo, RepoGit, RepoType

blue_print = Blueprint('repos', __name__, url_prefix='/api/v1/repos')


@blue_print.route('/', methods=['POST'])
def post():

    s = request.json
    repo = _request_body_to_repo(s)

    service.add(repo)
    return '', 201


@blue_print.route('/<name>', methods=['GET'])
def get(name: str):
    s = service.get(name)
    if not s:
        return '', 204

    return jsonify(s.__dict__()), 200


@blue_print.route('/', methods=['GET'])
def list_all():

    type_repo = request.args.get('type', None)

    if type_repo:
        result = service.list_all_by_type(RepoType(type_repo))
        return jsonify(result), 200

    return jsonify(service.list_all()), 200


@blue_print.route('/<name>', methods=['DELETE'])
def delete(name: str):
    service.delete(name)
    return '', 200


@blue_print.route('/types', methods=['GET'])
def list_types():
    return jsonify(service.list_types()), 200


@blue_print.route('/<name>', methods=['PUT'])
def modify(name: str):

    s = request.json
    repo = _request_body_to_repo(s)

    service.modify(name, repo)

    return '', 200


@blue_print.route('/<name>/pull', methods=['POST'])
def pull_repo_git(name):

    repo = service.get(name)

    if repo.type == RepoType.GIT:
        service.pull_repo_git(repo)

    return '', 200


@blue_print.route('/<name>/commit', methods=['POST'])
def commit_push_repo_git(name: str):

    commit_message = request.args.get('message', None)
    repo = service.get(name)

    if repo.type == RepoType.GIT:
        service.commit_push_repo_git(repo, commit_message)

    return '', 201


def _request_body_to_repo(s: Dict[str, Any]) -> Repo:

    repo = None
    type_repo = RepoType(s['type'])

    if type_repo == RepoType.LOCAL:
        repo = Repo(
            name=s['name']
        )

    if type_repo == RepoType.GIT:
        repo = RepoGit(
            name=s['name'],
            git_branch=s['branch'],
            git_path=s['path'],
            git_url=s['url'],
            git_user=s.get('user', None),
            git_pass=s.get('pass', None)
        )

    return repo


@blue_print.route('/<name>/yamls', methods=['GET'])
def export_repo(name: str):

    dict_objects = service.export_repo(name)
    dict_yaml = str(yaml.dump(dict_objects))

    name_yaml = datetime.now().isoformat() + '.yaml'

    return send_file(BytesIO(dict_yaml.encode()),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     download_name=ntpath.basename(name_yaml))


@blue_print.route('/<name>/zips', methods=['GET'])
def export_repo_zip(name: str):

    repo_zip = service.export_repo_zip(name)

    tar_name = datetime.now().isoformat() + '.tar.gz'

    return send_file(BytesIO(repo_zip),
                     mimetype='application/octet-stream',
                     as_attachment=True,
                     download_name=ntpath.basename(tar_name))
