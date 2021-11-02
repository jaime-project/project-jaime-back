import os
import shutil
import subprocess
from pathlib import Path

from logic.apps.modules.services import module_service
from logic.apps.servers.services import server_service


def setup_modules():

    names_modules = module_service.list_default()

    default_path = module_service.get_default_path()
    modules_path = module_service.get_path()

    if not os.path.exists(modules_path):
        os.makedirs(modules_path, exist_ok=True)

    for name in names_modules:
        shutil.copy(f'{default_path}/{name}.py', f'{modules_path}/{name}.py')


def setup_servers():

    yaml_path = server_service.get_path()

    if not os.path.exists(yaml_path):
        subprocess.getoutput(f"> {yaml_path}")
