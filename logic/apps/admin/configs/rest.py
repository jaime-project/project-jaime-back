from fastapi import FastAPI

from logic.apps.login import service as login_service
from logic.libs.rest.rest import setup


def setup_rest(app: FastAPI):
    setup(app, 'logic/apps/admin/routes')
    setup(app, 'logic/apps/*/route.*')


# def setup_token(app: FastAPI):

#     @app.before_request
#     def before_request():

#         no_login_paths = [
#             '/api/v1/login/',
#             '/',
#             '/vars',
#             '/api/v1/agents/'
#         ]

#         if request.method != 'OPTIONS' and request.path not in no_login_paths:

#             if not 'Authorization' in request.headers or not 'Bearer ' in request.headers['Authorization']:
#                 return '', 401

#             token = request.headers['Authorization'].replace('Bearer ', '')

#             if not login_service.is_a_valid_token(token):
#                 return '', 403
