from logic.apps.agents.services import agent_checker
from logic.apps.configs.services import config_service
from logic.apps.crons.services import cron_runner
from logic.apps.docs.services import doc_service
from logic.apps.modules.services import module_service
from logic.apps.repos.models.repo_model import Repo
from logic.apps.repos.services import repo_service
from logic.apps.works.services import work_runner, work_garbage_collector

_REPO_DEFAULT_NAME = 'local'
_MODULE_DEFAULT_NAME = 'test'


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
                           "print('Hellow world')", _REPO_DEFAULT_NAME)
        doc_service.add(_MODULE_DEFAULT_NAME,
                        "Module Example", _REPO_DEFAULT_NAME)


def start_threads():
    work_garbage_collector.start_garbage_collector_thread()
    agent_checker.start_agent_thread()
    work_runner.start_runner_thread()
    cron_runner.start_threads()


def setup_configs_vars():

    configs_vars = {
        'GARBAGE_COLLECTOR_RUN_MINUTES': '2880',
        'JAIME_USER': 'admin',
        'JAIME_PASS': 'admin',
    }

    for k, v in configs_vars.items():
        if not config_service.exist_config_var(k):
            config_service.update_config_var(k, v)
