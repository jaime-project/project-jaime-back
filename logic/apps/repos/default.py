from logic.apps.docs import service as doc_service
from logic.apps.markdown import service as markdown_service
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

_MD_DEFAULT_NAME = 'example'

_MD_DEFAULT_CONTENT = """
# Example markdown doc

## :package: Requeriments

* BASE agent

## :tada: How to use

* execute example by normal execution
"""


def setup_repos_default():

    repos_list = repo_service.list_all()

    if _REPO_DEFAULT_NAME not in repos_list:
        repo = Repo(name=_REPO_DEFAULT_NAME)
        repo_service.add(repo)

    if not module_service.get(_MODULE_DEFAULT_NAME, _REPO_DEFAULT_NAME):
        module_service.add(_MODULE_DEFAULT_NAME,
                           _MODULE_DEFAULT_CONTENT, _REPO_DEFAULT_NAME)

    if not doc_service.get(_MODULE_DEFAULT_NAME, _REPO_DEFAULT_NAME):
        doc_service.add(_MODULE_DEFAULT_NAME,
                        _DOCS_DEFAULT_CONTENT, _REPO_DEFAULT_NAME)

    if not markdown_service.get(_MODULE_DEFAULT_NAME, _REPO_DEFAULT_NAME):
        markdown_service.add(
            _MD_DEFAULT_NAME, _MD_DEFAULT_CONTENT, _REPO_DEFAULT_NAME)
