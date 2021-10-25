import threading
import time
from datetime import datetime, timedelta

from logic.apps.filesystem.services import workingdir_service
from logic.apps.processes.models.process_model import Status
from logic.apps.processes.services import process_service
from logic.libs.logger.logger import logger

_THREAD_GARBAGE_ACTIVE = True


def garbabge_collector():

    for id in process_service.list_all_running():

        process = process_service.get(id)

        if process.status != Status.RUNNING and (datetime.now() + timedelta(minutes=30) < process.end_date or process.status == Status.SUCCESS):
            process_service.delete_from_list(id)
            workingdir_service.delete(id)
            logger().info(f'Deleted workingdir -> {id}')


def start_garbage_thread():

    global _THREAD_GARBAGE_ACTIVE
    _THREAD_GARBAGE_ACTIVE = True

    def thread_method():
        global _THREAD_GARBAGE_ACTIVE
        while _THREAD_GARBAGE_ACTIVE:
            garbabge_collector()
            time.sleep(30)

    thread = threading.Thread(target=thread_method)
    thread.start()


def stop_garbage_thread():
    global _THREAD_GARBAGE_ACTIVE
    _THREAD_GARBAGE_ACTIVE = False
