from logic.apps.login.model import Login


def to_login(json: dict[str, object]) -> Login:
    return Login(json['user'], json['password'])
