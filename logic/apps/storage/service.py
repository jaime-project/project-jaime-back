import os

from logic.apps.admin.configs.variables import Vars, get_var
from logic.apps.storage.error import StorageError
from logic.apps.storage.model import FileDetail, FileList
from logic.libs.exception.exception import AppException
from datetime import datetime


def upload_file(file_name: str, path: str, content: bytes):

    full_path = os.path.join(get_var(Vars.STORAGE_PATH), path, file_name)
    with open(full_path, 'wb') as f:
        f.write(content)


def make_dir(dir_name: str, path: str):

    full_path = os.path.join(get_var(Vars.STORAGE_PATH), path, dir_name)
    os.system(f"mkdir -p {full_path}")


def download_file(file_name: str, path: str) -> bytes:

    full_path = os.path.join(get_var(Vars.STORAGE_PATH), path, file_name)
    with open(full_path, 'rb') as f:
        return f.read()


def list_all(path: str) -> FileList:

    file_list = FileList()

    full_path = os.path.join(get_var(Vars.STORAGE_PATH), path)

    for relative_path in os.listdir(full_path):

        if os.path.isdir(os.path.join(get_var(Vars.STORAGE_PATH), path, relative_path)):
            file_list.dirs.append(relative_path)
        else:
            file_list.files.append(relative_path)

    return file_list


def get_detail(path: str) -> FileDetail:

    full_path = os.path.join(get_var(Vars.STORAGE_PATH), path)

    return FileDetail(
        name=os.path.basename(full_path),
        last_modification=datetime.fromtimestamp(os.path.getmtime(full_path)),
        creation_date=datetime.fromtimestamp(os.path.getctime(full_path)),
        size=os.path.getsize(full_path),
    )


def delete(dir_or_file_name: str, path: str):

    full_path = os.path.join(
        get_var(Vars.STORAGE_PATH), path, dir_or_file_name)

    os.system(f"rm -fr {full_path}")


def put_dir_or_file(dir_or_file_name: str, path: str, new_name: str):

    full_path_old = os.path.join(
        get_var(Vars.STORAGE_PATH), path, dir_or_file_name)

    full_path_new = os.path.join(
        get_var(Vars.STORAGE_PATH), path, new_name)

    os.system(f"mv -f {full_path_old} {full_path_new}")
