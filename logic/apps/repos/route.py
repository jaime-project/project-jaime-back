from datetime import datetime
from typing import Any, Dict

import yaml
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.responses import Response

from logic.apps.repos import service
from logic.apps.repos.model import Repo, RepoGit, RepoType

apirouter = APIRouter(prefix='/api/v1/repos', tags=['Repos'])


@apirouter.route('/', methods=['POST'])
def post(s: Dict[str, object]):

    repo = _request_body_to_repo(s)

    service.add(repo)
    return JSONResponse('', 201)


@apirouter.route('/<name>', methods=['GET'])
def get(name: str):
    s = service.get(name)
    if not s:
        return '', 204

    return JSONResponse(s.__dict__()), 200


@apirouter.route('/', methods=['GET'])
def list_all(type: str = None):

    if type:
        result = service.list_all_by_type(RepoType(type))
        return JSONResponse(result), 200

    return JSONResponse(service.list_all()), 200


@apirouter.route('/<name>', methods=['DELETE'])
def delete(name: str):
    service.delete(name)
    return JSONResponse(JSONResponse('', 200))


@apirouter.route('/types', methods=['GET'])
def list_types():
    return JSONResponse(service.list_types()), 200


@apirouter.route('/<name>', methods=['PUT'])
def modify(name: str, s: Dict[str, object]):

    repo = _request_body_to_repo(s)

    service.modify(name, repo)

    return JSONResponse(JSONResponse('', 200))


@apirouter.route('/<name>/reload', methods=['POST'])
def reload(name):
    service.reload_repo_git(name)
    return JSONResponse(JSONResponse('', 200))


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


@apirouter.route('/<name>/yamls', methods=['GET'])
def export_modules_and_docs(name: str):

    dict_objects = service.export_modules_and_docs(name)
    dict_yaml = str(yaml.dump(dict_objects))

    name_yaml = datetime.now().isoformat() + '.yaml'

    headers = {
        'Content-Disposition': f'attachment; filename="{name_yaml}"'}

    return Response(
        open(dict_yaml, 'rb').read(),
        media_type='application/octet-stream',
        headers=headers
    )


@apirouter.route('/<name>/zips', methods=['GET'])
def export_modules_and_docs_zip(name: str):

    repo_zip = service.export_modules_and_docs_zip(name)

    tar_name = datetime.now().isoformat() + '.tar.gz'
    headers = {
        'Content-Disposition': f'attachment; filename="{tar_name}"'}

    return Response(
        open(repo_zip, 'rb').read(),
        media_type='application/octet-stream',
        headers=headers
    )
