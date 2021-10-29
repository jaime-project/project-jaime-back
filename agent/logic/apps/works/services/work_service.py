import time

import requests
from logic.apps.admin.config.variables import Vars, get_var
from logic.apps.filesystem.services import workingdir_service
from logic.libs.logger.logger import logger
from threading import Thread


def start(id: str, params_bytes: bytes, module_bytes: bytes, servers_bytes: bytes, tools_bytes: bytes):

    workingdir_service.create_by_id(id)

    base_path = workingdir_service.fullpath(id)

    with open(f'{base_path}/params.yaml', 'w') as f:
        f.write(params_bytes.decode())

    with open(f'{base_path}/module.py', 'w') as f:
        f.write(module_bytes.decode())

    with open(f'{base_path}/servers.yaml', 'w') as f:
        f.write(servers_bytes.decode())

    with open(f'{base_path}/tools.py', 'w') as f:
        f.write(tools_bytes.decode())

    _exec(id)


def _exec(id: str):

    base_path = workingdir_service.fullpath(id)


def connect_with_jaime():

    def thread_func():
        status_code = 0
        while status_code != 201:

            url = get_var(Vars.JAIME_URL)
            payload = {
                'host': get_var(Vars.PYTHON_HOST),
                'port': get_var(Vars.PYTHON_PORT),
                'type': get_var(Vars.AGENT_TYPE),
            }

            try:
                status_code = requests.post(
                    url, json=payload, verify=False, timeout=5).status_code

            except Exception:
                logger().error(f'Error en coneccion con Jaime -> reintentando en 5 seg')
                time.sleep(5)

        logger().info(
            f"Coneccion exitosa con Jaime -> URL: {get_var(Vars.JAIME_URL)}")

    thread = Thread(target=thread_func)
    thread.start()
