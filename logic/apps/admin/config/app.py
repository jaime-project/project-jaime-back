from logic.apps.agents.services import agent_checker
from logic.apps.crons.services import cron_runner
from logic.apps.repos.models.repo_model import Repo
from logic.apps.repos.services import repo_service
from logic.apps.works.services import work_runner

_REPO_DEFAULT_NAME = 'local'


def setup_repos():

    repos_list = repo_service.list_all()

    if _REPO_DEFAULT_NAME not in repos_list:
        repo_service.add(Repo(name=_REPO_DEFAULT_NAME))

    for repo_name in repos_list:
        if not repo_service.is_loaded(repo_name):
            repo_service.load_repo(repo_service.get(repo_name))


def start_threads():
    agent_checker.start_agent_thread()
    work_runner.start_runner_thread()
    cron_runner.start_threads()
