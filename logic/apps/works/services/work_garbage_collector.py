import threading
import time
from datetime import datetime, timedelta

from logic.apps.configs.services import config_service
from logic.apps.works.models.work_model import Status
from logic.apps.works.services import work_service
from logic.libs.logger.logger import logger

_THREAD_GARBAGE_COLLECTOR_ACTIVE = True
_MINUTES_VAR = 'GARBAGE_COLLECTOR_RUN_MINUTES'


def garbage_collector():

    try:
        works_ids = []
        works_ids += work_service.list_by_status(Status.CANCEL)
        works_ids += work_service.list_by_status(Status.ERROR)
        works_ids += work_service.list_by_status(Status.SUCCESS)
        
        for id in works_ids:

            work = work_service.get(id)
            minutes = int(config_service.get_config_var(_MINUTES_VAR))

            if work.start_date + timedelta(minutes=minutes) < datetime.now():
                work_service.delete(id)
                logger().info(
                    f'Borrando Job por garbage_collector -> id: {id}')

    except Exception as e:
        logger().error(str(e))


def start_garbage_collector_thread():

    logger().info('Iniciando hilo -> Garbage Collector')

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
