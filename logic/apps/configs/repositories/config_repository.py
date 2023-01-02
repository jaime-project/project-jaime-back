from typing import Dict, List

from logic.libs.sqliteAlchemy import sqliteAlchemy

from .entities.config_entity import ConfigEntity


def get_all() -> List[Dict[str, str]]:

    s = sqliteAlchemy.make_session()
    result = s.query(ConfigEntity).all()
    s.close()

    dict = {}
    for r in result:
        dict.update(r.to_model())

    return dict


def get(key: str) -> Dict[str, str]:

    s = sqliteAlchemy.make_session()
    result = s.query(ConfigEntity).get({'key': key})
    s.close()

    if result:
        return result.to_model()

    return None


def add(key: str, value: str):

    s = sqliteAlchemy.make_session()

    e = ConfigEntity.from_model(key, value)
    s.add(e)

    s.commit()
    s.flush()


def delete(key: str):

    if not exist(key):
        return

    s = sqliteAlchemy.make_session()
    e = s.query(ConfigEntity).get({'key': key})
    s.delete(e)

    s.commit()
    s.flush()


def exist(key: str) -> bool:

    result = True

    s = sqliteAlchemy.make_session()
    if s.query(ConfigEntity).filter_by(key=key).count() == 0:
        result = False

    s.close()
    return result
