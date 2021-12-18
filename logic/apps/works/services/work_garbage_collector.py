import threading
import time
from datetime import datetime, timedelta

from logic.apps.agents.errors.agent_error import AgentError
from logic.apps.agents.services import agent_service
from logic.apps.works.models.work_model import Status
from logic.apps.works.services import work_service
from logic.libs.exception.exception import AppException
from logic.libs.logger.logger import logger

_THREAD_GARBAGE_COLLECTOR_ACTIVE = True


def garbage_collector():

    for id in list(work_service.list_all()):

        work = work_service.get(id)
        if work.status != Status.TERMINATED:
            continue

        if work.terminated_date + timedelta(hours=24) < datetime.now():
            work_service.delete(id)
            agent_service.delete_work(id)
            logger().info(f'Borrando proceso TERMINATED -> id: {id}')


def start_runner_thread():

    logger().info('Iniciando hilo -> garbage collector')

    global _THREAD_GARBAGE_COLLECTOR_ACTIVE
    _THREAD_GARBAGE_COLLECTOR_ACTIVE = True

    def thread_method():
        global _THREAD_GARBAGE_COLLECTOR_ACTIVE
        while _THREAD_GARBAGE_COLLECTOR_ACTIVE:
            garbage_collector()
            time.sleep(30)

    thread = threading.Thread(target=thread_method)
    thread.start()


def stop_runner_thread():
    global _THREAD_GARBAGE_COLLECTOR_ACTIVE
    _THREAD_GARBAGE_COLLECTOR_ACTIVE = False
