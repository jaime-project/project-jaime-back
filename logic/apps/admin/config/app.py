from logic.apps.repos.models.repo_model import Repo, RepoGit, RepoType
from logic.apps.repos.services import repo_service

_REPO_DEFAULT_NAME = 'local'


def setup_repos():

    repos_list = repo_service.list_all()

    for repo_name in repos_list:
        if not repo_service.is_loaded(repo_name):
            repo_service.load_repo(repo_service.get(repo_name))


def setup_repos_default():

    repos_list = repo_service.list_all()

    if _REPO_DEFAULT_NAME not in repos_list:
        repo_service.add(Repo(name=_REPO_DEFAULT_NAME))
