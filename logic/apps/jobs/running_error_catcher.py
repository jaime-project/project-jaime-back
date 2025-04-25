import threading
import time

from logic.apps.agents import service as agent_service
from logic.apps.jobs import service as jobs_service
from logic.apps.jobs.model import Status
from logic.libs.logger import logger

_THREAD_RUNING_ERROR_CATCHER_ACTIVE = True


def running_error_catcher():

    try:
        for id in jobs_service.list_by_status(Status.RUNNING):

            job = jobs_service.get(id)

            if not agent_service.get(job.agent.id):
                jobs_service.change_status(id, Status.UNFINISHED)
                logger.log.warning(
                    f'Status job Changed to UNFINISHED by its agent is down -> {job.name} - {id}')

    except Exception as e:
        logger.log.error(e)


def start_running_error_catcher_thread():

    logger.log.info('Start thread -> Running Error Catcher')

    global _THREAD_RUNING_ERROR_CATCHER_ACTIVE
    _THREAD_RUNING_ERROR_CATCHER_ACTIVE = True

    def thread_method():
        global _THREAD_RUNING_ERROR_CATCHER_ACTIVE
        while _THREAD_RUNING_ERROR_CATCHER_ACTIVE:
            running_error_catcher()
            time.sleep(3)

    thread = threading.Thread(target=thread_method)
    thread.start()


def stop_running_error_catcher_thread():
    global _THREAD_RUNING_ERROR_CATCHER_ACTIVE
    _THREAD_RUNING_ERROR_CATCHER_ACTIVE = False
