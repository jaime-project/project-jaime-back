import ntpath
import os

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from starlette.responses import Response

from logic.apps.admin.configs.variables import Vars
from logic.libs.variables.variables import all_vars, get_var

apirouter = APIRouter(prefix='', tags=['Admin'])


@apirouter.route('/vars')
def get_vars():
    return JSONResponse(all_vars())


@apirouter.route('/')
def alive():
    version = get_var(Vars.VERSION)
    return JSONResponse(version=version)


@apirouter.route('/postman')
def get_postman():
    postman_files = sorted([
        f for f in os.listdir('logic/resources/')
        if str(f).endswith('.postman_collection.json')
    ], reverse=True)

    collection_dir = next(iter(postman_files), None)
    headers = {
        'Content-Disposition': f'attachment; filename="{ntpath.basename(collection_dir)}"'}

    return Response(
        open(collection_dir, 'rb').read(),
        media_type='application/octet-stream',
        headers=headers
    )
