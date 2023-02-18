from typing import Dict, List

from logic.apps.messages import repository
from logic.apps.messages.error import MessageError
from logic.apps.messages.model import Message, Status
from logic.libs.exception.exception import AppException
from logic.apps.admin.configs.variables import get_var, Vars


def add(message: Message):

    if repository.exist(message.id):
        msj = f"Message with name {message.id} already exist"
        raise AppException(MessageError.MESSAGE_ALREADY_EXISTS_ERROR, msj)

    repository.add(message)


def get(id: str) -> Message:

    if not repository.exist(id):
        return None

    message = repository.get(id)
    message.status = Status.SEEN

    delete(message.id)
    add(message)

    return message


def list_all() -> List[str]:

    return [
        s.id
        for s in repository.get_all()
    ]


def list_status() -> List[str]:
    return [s.value for s in Status]


def get_all() -> List[Message]:
    return repository.get_all()


def get_all_short(size: int = 10, page: int = 1, filter: str = None, order: str = None) -> List[Dict[str, str]]:

    return [
        {
            "title": s.title,
            "subject": s.subject,
            "date": s.date,
            "status": s.status.value,
            "job": s.job,
            "id": s.id,
        }
        for s in repository.get_all(size, page, filter, order)
    ]


def delete(id: str):

    if not repository.exist(id):
        msj = f"Message with id {id} not exist"
        raise AppException(MessageError.MESSAGE_NOT_EXISTS_ERROR, msj)

    repository.delete(id)


def get_file(id: str, path: str) -> bytes:

    if not repository.exist(id):
        msj = f"Message with id {id} not exist"
        raise AppException(MessageError.MESSAGE_NOT_EXISTS_ERROR, msj)

    message = get(id)
    final_path = f'{get_var(Vars.WORKINGDIR_PATH)}/{message.job}/{path}'.replace('//', '/')

    with open(final_path, 'rb') as file:
        return file.read()


def list_by_status(status: Status) -> List[str]:
    return [
        m.id
        for m
        in repository.get_all_by_status(status)
    ]


def delete_by_status(status: Status):
    for id in list_by_status(status):
        delete(id)
