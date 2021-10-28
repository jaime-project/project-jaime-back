import threading
import time

from logic.apps.nodes.services import node_service
from logic.libs.logger.logger import logger

_THREAD_NODE_ACTIVE = True


def check_node_alive():

    for id in node_service.list_all().keys():

        tries = 0
        while tries < 3:
            if node_service.is_alive(id):
                break
            else:
                tries += 1
                time.sleep(1)

            if tries == 3:
                node_service.delete(id)
                logger().info(f'Deleted node because its ofline -> {id}')


def start_node_thread():

    global _THREAD_NODE_ACTIVE
    _THREAD_NODE_ACTIVE = True

    def thread_method():
        global _THREAD_NODE_ACTIVE
        while _THREAD_NODE_ACTIVE:
            check_node_alive()
            time.sleep(5)

    thread = threading.Thread(target=thread_method)
    thread.start()


def stop_node_thread():
    global _THREAD_NODE_ACTIVE
    _THREAD_NODE_ACTIVE = False
