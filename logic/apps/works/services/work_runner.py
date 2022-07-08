import threading
import time
from datetime import datetime

from logic.apps.agents.models.agent_model import AgentStatus
from logic.apps.agents.services import agent_service
from logic.apps.works.models.work_model import Status
from logic.apps.works.services import work_service
from logic.libs.logger.logger import logger

_THREAD_RUNNER_ACTIVE = True


def runner():

    try:

        for id in work_service.list_by_status(Status.READY):

            work = work_service.get(id)

            agent = agent_service.get_available_agent_by_type(work.agent_type)
            if not agent:
                continue

            agent_service.change_status(agent.id, AgentStatus.WORKING)

            work.agent = agent
            work.status = Status.RUNNING
            work.running_date = datetime.now()

            work_service.modify(work)

            work_service.exec_into_agent(work)

    except Exception as e:
        logger().error(e)


def start_runner_thread():

    logger().info('Iniciando hilo -> runner')

    global _THREAD_RUNNER_ACTIVE
    _THREAD_RUNNER_ACTIVE = True

    def thread_method():
        global _THREAD_RUNNER_ACTIVE
        while _THREAD_RUNNER_ACTIVE:
            runner()
            time.sleep(3)

    thread = threading.Thread(target=thread_method)
    thread.start()


def stop_runner_thread():
    global _THREAD_RUNNER_ACTIVE
    _THREAD_RUNNER_ACTIVE = False
