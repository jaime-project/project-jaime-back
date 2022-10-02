from datetime import datetime, timedelta
from lib2to3.pgen2.tokenize import TokenError
from uuid import uuid4

from logic.apps.configs.services import config_service
from logic.apps.login.errors.login_error import LoginError
from logic.libs.exception.exception import AppException

_CURRENTS_LOGINS = {}

_JAIME_USER_CONFIG = 'JAIME_USER'
_JAIME_PASS_CONFIG = 'JAIME_PASS'


def login(user: str, password: str) -> str:

    _update_currents_logins()

    config_user = config_service.get_config_var(_JAIME_USER_CONFIG)
    config_pass = config_service.get_config_var(_JAIME_PASS_CONFIG)

    if user != config_user or password != config_pass:
        raise AppException(LoginError.USER_OR_PASS_ERROR,
                           'User or pass is invalid')

    return get_token()


def _update_currents_logins():

    tokens_to_delete = []

    global _CURRENTS_LOGINS
    for token, date in _CURRENTS_LOGINS.items():
        if date + timedelta(minutes=15) >= datetime.now():
            tokens_to_delete.append(token)

    for token in tokens_to_delete:
        _CURRENTS_LOGINS.pop(token)


def is_a_valid_token(token: str) -> bool:

    global _CURRENTS_LOGINS

    if token not in _CURRENTS_LOGINS:
        return False

    _CURRENTS_LOGINS[token] = datetime.now()
    return True


def get_token() -> str:

    token = str(uuid4()).replace('-', '')

    global _CURRENTS_LOGINS
    _CURRENTS_LOGINS[token] = datetime.now()

    return token
