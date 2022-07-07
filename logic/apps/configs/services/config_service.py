import os
from pathlib import Path

import requests

from logic.apps.filesystem.services import filesystem_service
from logic.apps.agents.services import agent_service

_REQUIREMENTS_FILE_PATH = f'{Path.home()}/.jaime/requirements.txt'


def updateRequirements(content: str):

    filesystem_service.delete_file(get_requirements_path())
    filesystem_service.create_file(get_requirements_path(), content)

    for agent in agent_service.list_all():

        url = f'{agent.get_url()}/api/v1/configs/requirements'
        requests.post(url, data=content, verify=False)


def getRequirements() -> str:

    if not os.path.exists(get_requirements_path()):
        filesystem_service.create_file(get_requirements_path(), '')

    return filesystem_service.get_file_content(get_requirements_path())


def get_requirements_path() -> str:

    global _REQUIREMENTS_FILE_PATH
    return _REQUIREMENTS_FILE_PATH
