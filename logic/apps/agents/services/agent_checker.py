import threading
import time

from logic.apps.agents.services import agent_service
from logic.libs.logger.logger import logger

_THREAD_NODE_ACTIVE = True


def check_node_alive():

    for n in agent_service.list_all():

        tries = 0
        while tries < 3:
            if agent_service.is_alive(n.id):
                break
            else:
                tries += 1
                time.sleep(1)

            if tries == 3:
                agent_service.delete(n.id)
                logger().info(f'Deleted node by long time ofline -> {n.id}')


def start_agent_thread():

    global _THREAD_NODE_ACTIVE
    _THREAD_NODE_ACTIVE = True

    def thread_method():
        global _THREAD_NODE_ACTIVE
        while _THREAD_NODE_ACTIVE:
            check_node_alive()
            time.sleep(10)

    thread = threading.Thread(target=thread_method)
    thread.start()


def stop_node_thread():
    global _THREAD_NODE_ACTIVE
    _THREAD_NODE_ACTIVE = False