from logic.apps.agents import checker as agent_checker
from logic.apps.configs import service
from logic.apps.crons import runner as cron_runner
from logic.apps.docs import service as doc_service
from logic.apps.jobs import garbage_collector as job_garbage
from logic.apps.jobs import runner as job_runner
from logic.apps.jobs import running_error_catcher
from logic.apps.modules import service as module_service
from logic.apps.repos import service as repo_service
from logic.apps.repos.model import Repo

_REPO_DEFAULT_NAME = 'example'

_MODULE_DEFAULT_NAME = 'example'
_MODULE_DEFAULT_CONTENT = """import tools

params = tools.get_params()
who = params['person']['name']
tools.log.info(f'Hello {who}')
"""
_DOCS_DEFAULT_CONTENT = """person:
    name: Jaime
"""


def setup_repos():

    repos_list = repo_service.list_all()

    if _REPO_DEFAULT_NAME not in repos_list:
        repo_service.add(Repo(name=_REPO_DEFAULT_NAME))

    for repo_name in repos_list:
        if not repo_service.is_loaded(repo_name):
            repo_service.load_repo(repo_service.get(repo_name))

    module_default_exist = module_service.get(
        _MODULE_DEFAULT_NAME, _REPO_DEFAULT_NAME) != None

    if not module_default_exist:

        module_service.add(_MODULE_DEFAULT_NAME,
                           _MODULE_DEFAULT_CONTENT, _REPO_DEFAULT_NAME)
        doc_service.add(_MODULE_DEFAULT_NAME,
                        _DOCS_DEFAULT_CONTENT, _REPO_DEFAULT_NAME)


def start_threads():
    job_garbage.start_garbage_collector_thread()
    agent_checker.start_agent_thread()
    job_runner.start_runner_thread()
    cron_runner.start_threads()
    running_error_catcher.start_running_error_catcher_thread()


def setup_configs_vars():

    configs_vars = {
        'GARBAGE_COLLECTOR_RUN_MINUTES': '2880',
        'JAIME_USER': 'admin',
        'JAIME_PASS': 'admin',
    }

    for k, v in configs_vars.items():
        if not service.exist_config_var(k):
            service.update_config_var(k, v)
