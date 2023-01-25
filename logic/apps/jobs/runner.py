import threading
import time
from datetime import datetime

from logic.apps.agents import service as agent_service
from logic.apps.agents.model import AgentStatus
from logic.apps.jobs import service as jobs_service
from logic.apps.jobs.model import Status
from logic.libs.logger import logger

_THREAD_RUNNER_ACTIVE = True


def runner():

    try:

        for id in jobs_service.list_by_status(Status.READY):

            job = jobs_service.get(id)

            agent = agent_service.get_available_agent_by_type(job.agent_type)
            if not agent:
                continue

            agent_service.change_status(agent.id, AgentStatus.WORKING)

            job.agent = agent
            job.status = Status.RUNNING
            job.running_date = datetime.now()

            jobs_service.modify(job)

            jobs_service.exec_into_agent(job)

    except Exception as e:
        logger.log.error(e)


def start_runner_thread():

    logger.log.info('Start thread -> runner')

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
