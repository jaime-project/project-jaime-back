import threading
import time
from datetime import datetime, timedelta

from logic.apps.works.models.work_model import Status
from logic.apps.works.services import work_service
from logic.libs.logger.logger import logger

_THREAD_GARBAGE_ACTIVE = True


def garbabge_collector():

    for id in work_service.list_all_running():

        work = work_service.get(id)

        delete = (work.status == Status.ERROR and datetime.now() + timedelta(minutes=30) < work.end_date) or (
            work.status == Status.SUCCESS and datetime.now() + timedelta(minutes=5) < work.end_date)

        if delete:
            work_service.delete(id)
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
