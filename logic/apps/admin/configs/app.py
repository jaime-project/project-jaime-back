import os

from logic.apps.admin.configs.variables import Vars, get_var
from logic.apps.agents import checker as agent_checker
from logic.apps.crons import runner as cron_runner
from logic.apps.jobs import garbage_collector as job_garbage
from logic.apps.jobs import runner as job_runner
from logic.apps.jobs import running_error_catcher
from logic.apps.repos import default as repo_default


def setup_directories():
    if not os.path.exists(get_var(Vars.JAIME_HOME_PATH)):
        os.makedirs(get_var(Vars.JAIME_HOME_PATH))

    if not os.path.exists(get_var(Vars.WORKINGDIR_PATH)):
        os.makedirs(get_var(Vars.WORKINGDIR_PATH))

    if not os.path.exists(get_var(Vars.STORAGE_PATH)):
        os.makedirs(get_var(Vars.STORAGE_PATH))


def setup_repos():
    repo_default.setup_repos_default()


def start_threads():
    job_garbage.start_garbage_collector_thread()
    agent_checker.start_agent_thread()
    job_runner.start_runner_thread()
    cron_runner.start_threads()
    running_error_catcher.start_running_error_catcher_thread()
