import os
from datetime import datetime

from logic.apps.admin.configs.variables import Vars, get_var
from logic.apps.storage.model import FileDetail, FileList


def upload_file(file_name: str, path: str, content: bytes):

    full_dir_path = _full_path(path)

    if not os.path.exists(full_dir_path):
        os.system(f"mkdir -p {full_dir_path}")

    with open(_full_path(path, file_name), 'wb') as f:
        f.write(content)


def make_dir(dir_name: str, path: str):

    os.system(f"mkdir -p {_full_path(path, dir_name)}")


def download_file(file_name: str, path: str) -> bytes:

    with open(_full_path(path, file_name), 'rb') as f:
        return f.read()


def list_all(path: str = "/", filter: str = None) -> FileList:

    file_list = FileList()

    for relative_path in os.listdir(_full_path(path)):

        if os.path.isdir(os.path.join(_full_path(path), relative_path)):
            file_list.dirs.append(relative_path)
        else:
            file_list.files.append(relative_path)

    if filter:

        file_list.dirs = [
            d
            for d in file_list.dirs
            if filter in d
        ]

        file_list.files = [
            f
            for f in file_list.files
            if filter in f
        ]

    return file_list


def get_detail(path: str) -> FileDetail:

    full_path = _full_path(path)

    return FileDetail(
        name=os.path.basename(full_path),
        last_modification=datetime.fromtimestamp(os.path.getmtime(full_path)),
        creation_date=datetime.fromtimestamp(os.path.getctime(full_path)),
        size=os.path.getsize(full_path),
    )


def delete(dir_or_file_name: str, path: str):

    os.system(f"""rm -fr "{_full_path(path, dir_or_file_name)}" """)


def put_dir_or_file(dir_or_file_name: str, path: str, new_name: str):

    full_path_old = _full_path(path, dir_or_file_name)
    full_path_new = _full_path(path, new_name)

    os.system(f"mv -f {full_path_old} {full_path_new}")


def _full_path(path: str = "/", sub_path: str = None) -> str:

    full_path = get_var(Vars.STORAGE_PATH)

    if path != "/":
        full_path += f"/{path}"

    if sub_path:
        full_path += f"/{sub_path}"

    return full_path
