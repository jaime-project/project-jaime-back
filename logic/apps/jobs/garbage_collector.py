from logic.apps.admin.configs.variables import get_var, Vars
import threading
import time
from datetime import datetime, timedelta

from logic.apps.jobs import service
from logic.apps.jobs.model import Status
from logic.libs.logger import logger

_THREAD_GARBAGE_COLLECTOR_ACTIVE = True


def garbage_collector():

    try:
        works_ids = []
        works_ids += service.list_by_status(Status.CANCEL)
        works_ids += service.list_by_status(Status.ERROR)
        works_ids += service.list_by_status(Status.SUCCESS)

        for id in works_ids:

            job = service.get(id)
            minutes = int(get_var(Vars.DELETE_OLD_JOBS_MINUTES))

            if job.start_date + timedelta(minutes=minutes) < datetime.now():
                service.delete(id)
                logger.log.info(
                    f'Deleting Job by garbage_collector -> id: {id}')

    except Exception as e:
        logger.log.error(str(e))


def start_garbage_collector_thread():

    logger.log.info('Start thread -> Garbage Collector')

    global _THREAD_GARBAGE_COLLECTOR_ACTIVE
    _THREAD_GARBAGE_COLLECTOR_ACTIVE = True

    def thread_method():
        global _THREAD_GARBAGE_COLLECTOR_ACTIVE
        while _THREAD_GARBAGE_COLLECTOR_ACTIVE:
            garbage_collector()
            time.sleep(3)

    thread = threading.Thread(target=thread_method)
    thread.start()


def stop_runner_thread():
    global _THREAD_GARBAGE_COLLECTOR_ACTIVE
    _THREAD_GARBAGE_COLLECTOR_ACTIVE = False
