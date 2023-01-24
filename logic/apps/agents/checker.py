import threading
import time

from logic.apps.agents import service
from logic.libs.logger import logger

_THREAD_AGENT_ACTIVE = True


def check_node_alive():

    for n in list(service.list_all()):

        tries = 0
        while tries < 3:
            if service.is_alive(n.id):
                break
            else:
                tries += 1
                time.sleep(2)

            if tries == 3:
                service.delete(n.id)
                logger.log.info(f'Delete agent by offline -> {n.id}')


def start_agent_thread():

    logger.log.info('Start thread -> Agent')

    global _THREAD_AGENT_ACTIVE
    _THREAD_AGENT_ACTIVE = True

    def thread_method():
        global _THREAD_AGENT_ACTIVE
        while _THREAD_AGENT_ACTIVE:
            check_node_alive()
            time.sleep(5)

    thread = threading.Thread(target=thread_method)
    thread.start()


def stop_node_thread():
    global _THREAD_AGENT_ACTIVE
    _THREAD_AGENT_ACTIVE = False
