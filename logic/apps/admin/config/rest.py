from flask import Flask
from logic.libs.rest import rest


def setup_rest(app: Flask) -> Flask:

    rest.setup(app, 'logic/apps/*/routes')
