import threading
import time
from uuid import UUID

from logic.apps.filesystem.services import workingdir_service
from logic.libs.logger.logger import logger

_pipelines_runned = []
_thread_garbage_active = True


def garbabge_collector():

    global _pipelines_runned

    for id in _pipelines_runned:
        workingdir_service.delete(id)
        logger().info(f'Deleted workingdir -> {id}')

    _pipelines_runned = []


def start_garbage_thread():

    global _thread_garbage_active
    _thread_garbage_active = True

    def thread_method():
        global _thread_garbage_active
        while _thread_garbage_active:
            garbabge_collector()
            time.sleep(30)

    thread = threading.Thread(target=thread_method)
    thread.start()


def stop_garbage_thread():
    global _thread_garbage_active
    _thread_garbage_active = False


def add_pipeline_runned(id: UUID):
    global _pipelines_runned
    _pipelines_runned.append(id)
