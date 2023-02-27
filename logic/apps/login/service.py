from datetime import datetime, timedelta
from uuid import uuid4

from logic.apps.admin.configs.variables import Vars, get_var
from logic.apps.login.error import LoginError
from logic.apps.login.model import Login
from logic.libs.exception.exception import AppException

_CURRENTS_LOGINS = {}


def login(login: Login) -> str:

    config_user = get_var(Vars.JAIME_USER)
    config_pass = get_var(Vars.JAIME_PASS)

    if login.user != config_user or login.password != config_pass:
        raise AppException(LoginError.USER_OR_PASS_ERROR,
                           'User or pass is invalid')

    return get_token()


def _update_currents_tokens():

    tokens_to_delete = []

    global _CURRENTS_LOGINS
    for token, date in _CURRENTS_LOGINS.items():
        if date + timedelta(minutes=15) <= datetime.now():
            tokens_to_delete.append(token)

    for token in tokens_to_delete:
        _CURRENTS_LOGINS.pop(token)


def is_a_valid_token(token: str) -> bool:

    _update_currents_tokens()

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
