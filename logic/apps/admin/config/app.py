from logic.apps.repos.models.repo_model import Repo, RepoGit, RepoType
from logic.apps.repos.services import repo_service

_REPO_DEFAULT_NAME = 'local'

_REPO_GIT_DEFAULT_NAME = 'ocp_migrate'
_REPO_GIT_DEFAULT_URL = 'https://github.com/brianwolf/project-jaime.git'
_REPO_GIT_DEFAULT_PATH = '/repo_modules_default'
_REPO_GIT_DEFAULT_USER = 'brianwolf94'
_REPO_GIT_DEFAULT_PASS = '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'
_REPO_GIT_DEFAULT_BRANCH = 'main'


def setup_repos():

    repos_list = repo_service.list_all_by_type(RepoType.GIT)

    for repo_name in repos_list:
        if repo_service.is_downloaded(repo_name):
            continue

        repo_service.download_git_repo(repo_service.get(repo_name))


def setup_repos_default():

    repos_list = repo_service.list_all()

    if _REPO_DEFAULT_NAME not in repos_list:
        repo_service.add(Repo(name=_REPO_DEFAULT_NAME))

    if _REPO_DEFAULT_NAME not in repos_list:
        repo_service.add(RepoGit(
            name=_REPO_GIT_DEFAULT_NAME,
            git_user=_REPO_GIT_DEFAULT_USER,
            git_pass=_REPO_GIT_DEFAULT_PASS,
            git_path=_REPO_GIT_DEFAULT_PATH,
            git_branch=_REPO_GIT_DEFAULT_BRANCH,
            git_url=_REPO_GIT_DEFAULT_URL))
