from logic.apps.agents import checker as agent_checker
from logic.apps.crons import runner as cron_runner
from logic.apps.jobs import garbage_collector as job_garbage
from logic.apps.jobs import runner as job_runner
from logic.apps.jobs import running_error_catcher
from logic.apps.repos import default as repo_default


def setup_repos():
    repo_default.setup_repos_default()


def start_threads():
    job_garbage.start_garbage_collector_thread()
    agent_checker.start_agent_thread()
    job_runner.start_runner_thread()
    cron_runner.start_threads()
    running_error_catcher.start_running_error_catcher_thread()
