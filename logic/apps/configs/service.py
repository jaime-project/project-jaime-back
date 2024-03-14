import os
from datetime import datetime
from typing import Dict, List

import requests

from logic.apps.admin.configs.logger import get_logs_path
from logic.apps.admin.configs.variables import Vars, get_var
from logic.apps.agents import service as agent_service
from logic.apps.agents.error import AgentError
from logic.apps.cards import service as card_service
from logic.apps.clusters import service as cluster_service
from logic.apps.clusters.model import Cluster
from logic.apps.configs.error import ObjectError
from logic.apps.crons import service as cron_service
from logic.apps.crons.model import CronJob, CronStatus
from logic.apps.docs import service as doc_service
from logic.apps.filesystem import filesystem_service
from logic.apps.hooks import service as hook_service
from logic.apps.markdown import service as markdown_service
from logic.apps.messages import service as message_service
from logic.apps.messages.model import Message, Status
from logic.apps.modules import service as module_service
from logic.apps.repos import service as repo_service
from logic.apps.repos.model import Repo, RepoGit
from logic.apps.servers import service as server_service
from logic.apps.servers.model import Server
from logic.libs.exception.exception import AppException
from logic.libs.logger import logger
from logic.apps.hooks.model import HookJob, HookStatus
from logic.apps.cards.model import Card


def update_requirements(content: str):
    filesystem_service.delete_file(get_requirements_path())
    filesystem_service.create_file(get_requirements_path(), content)

    for agent in agent_service.list_all():
        try:
            url = f"{agent.get_url()}/api/v1/configs/requirements"
            requests.post(url, data=content, verify=False)

        except Exception as e:
            logger.log.error(
                "Error in connection with agent to update pip dependencies", e
            )


def get_requirements() -> str:
    if not os.path.exists(get_requirements_path()):
        filesystem_service.create_file(get_requirements_path(), "")

    return filesystem_service.get_file_content(get_requirements_path())


def get_requirements_path() -> str:
    return f"{get_var(Vars.JAIME_HOME_PATH)}/requirements.txt"


def get_jaime_logs() -> str:
    return filesystem_service.get_file_content(get_logs_path())


def get_agent_logs(agent_id: str) -> str:
    agent = agent_service.get(agent_id)
    if not agent:
        raise AppException(
            AgentError.AGENT_NOT_EXIST_ERROR, f"Agent with id {agent_id} not found"
        )

    url = agent.get_url() + f"/api/v1/configs/logs"
    response = requests.get(url, verify=False)

    return response.text


def get_all_objects() -> Dict[str, List[Dict[str, str]]]:
    objects = {}

    objects["servers"] = [
        o.__dict__() for o in server_service.get_all(size=None, page=None)
    ]

    objects["clusters"] = [
        o.__dict__() for o in cluster_service.get_all(size=None, page=None)
    ]

    objects["crons"] = [
        o.__dict__() for o in cron_service.get_all(size=None, page=None)
    ]

    objects["hooks"] = [
        o.__dict__() for o in hook_service.get_all(size=None, page=None)
    ]

    objects["cards"] = [
        o.__dict__() for o in card_service.get_all(filter=None)
    ]

    objects["repos"] = [o.__dict__() for o in repo_service.get_all()]

    objects["modules"] = []
    for repo in objects["repos"]:
        for module_name in module_service.list_all(repo["name"]):
            objects["modules"].append(
                {
                    "repo": repo["name"],
                    "name": module_name,
                    "content": module_service.get(module_name, repo["name"]),
                }
            )

    objects["docs"] = []
    for repo in objects["repos"]:
        for doc_name in doc_service.list_all(repo["name"]):
            objects["docs"].append(
                {
                    "repo": repo["name"],
                    "name": doc_name,
                    "content": doc_service.get(doc_name, repo["name"]),
                }
            )

    objects["markdowns"] = []
    for repo in objects["repos"]:
        for md_name in markdown_service.list_all(repo["name"]):
            objects["markdowns"].append(
                {
                    "repo": repo["name"],
                    "name": md_name,
                    "content": markdown_service.get(md_name, repo["name"]),
                }
            )

    objects["requirements"] = get_requirements()

    objects["messages"] = [m.__dict__() for m in message_service.get_all()]

    return objects


def update_objects(objects: Dict[str, str], replace: bool = False):
    try:
        _create_and_update_objects(objects, replace)

    except Exception as e:
        raise AppException(ObjectError.CREATION_OBJECTS_ERROR, str(e), e)


def _create_and_update_objects(objects: Dict[str, str], replace: bool):
    if "clusters" in objects:
        for o in objects["clusters"]:
            cluster = Cluster(
                name=o["name"],
                url=o["url"],
                token=o["token"],
                type=o["type"],
            )

            if replace and cluster_service.get(cluster.name):
                cluster_service.delete(cluster.name)
                cluster_service.add(cluster)

            if not cluster_service.get(cluster.name):
                cluster_service.add(cluster)

    if "servers" in objects:
        for o in objects["servers"]:
            server = Server(
                name=o["name"],
                host=o["host"],
                port=o["port"],
                user=o["user"],
                password=o["password"],
            )

            if replace and server_service.get(server.name):
                server_service.delete(server.name)
                server_service.add(server)

            if not server_service.get(server.name):
                server_service.add(server)

    if "crons" in objects:
        for o in objects["crons"]:
            cronJob = CronJob(
                name=o["name"],
                cron_expression=o["cron_expression"],
                job_module_repo=o["job_module_repo"],
                job_module_name=o["job_module_name"],
                job_agent_type=o["job_agent_type"],
                id=o["id"],
                creation_date=datetime.fromisoformat(o["creation_date"]),
                status=CronStatus(o["status"]),
                job_params=o["job_params"],
            )

            if replace and cron_service.get(cronJob.id):
                cron_service.delete(cronJob.id)
                cron_service.add(cronJob)

            if not cron_service.get(cronJob.id):
                cron_service.add(cronJob)

    if "hooks" in objects:
        for o in objects["hooks"]:
            hookJob = HookJob(
                name=o["name"],
                job_module_repo=o["job_module_repo"],
                job_module_name=o["job_module_name"],
                job_agent_type=o["job_agent_type"],
                id=o["id"],
                status=HookStatus(o["status"]),
                creation_date=datetime.fromisoformat(o["creation_date"]),
                job_params=o["job_params"],
            )

            if replace and hook_service.get(hookJob.id):
                hook_service.delete(hookJob.id)
                hook_service.add(hookJob)

            if not hook_service.get(hookJob.id):
                hook_service.add(hookJob)

    if "cards" in objects:
        for o in objects["cards"]:
            card = Card(
                name=o["name"],
                description=o["description"],
                color=o["color"],
                job_module_repo=o["job_module_repo"],
                job_module_name=o["job_module_name"],
                job_agent_type=o["job_agent_type"],
                job_default_docs=o["job_default_docs"],
                job_card_docs=o["job_card_docs"],
                id=o["id"],
                creation_date=datetime.fromisoformat(o["creation_date"]),
            )

            if replace and card_service.get(card.id):
                card_service.delete(card.id)
                card_service.add(card)

            if not card_service.get(card.id):
                card_service.add(card)

    if "repos" in objects:
        for o in objects["repos"]:
            repo = Repo(
                name=o["name"],
            )

            if "git_url" in o:
                repo = RepoGit(
                    name=o["name"],
                    git_path=o["git_path"],
                    git_user=o["git_user"],
                    git_pass=o["git_pass"],
                    git_url=o["git_url"],
                    git_branch=o["git_branch"],
                )

            if replace and repo_service.get(repo.name):
                repo_service.delete(repo.name)
                repo_service.add(repo)

            if not repo_service.get(repo.name):
                repo_service.add(repo)

    if "modules" in objects:
        for o in objects["modules"]:
            name = o["name"]
            content = o["content"]
            repo = o["repo"]

            if replace and module_service.get(name, repo):
                module_service.delete(name, repo)
                module_service.add(name, content, repo)

            if not module_service.get(name, repo):
                module_service.add(name, content, repo)

    if "docs" in objects:
        for o in objects["docs"]:
            name = o["name"]
            content = o["content"]
            repo = o["repo"]

            if replace and doc_service.get(name, repo):
                doc_service.delete(name, repo)
                doc_service.add(name, content, repo)

            if not doc_service.get(name, repo):
                doc_service.add(name, content, repo)

    if "markdowns" in objects:
        for o in objects["markdowns"]:
            name = o["name"]
            content = o["content"]
            repo = o["repo"]

            if replace and markdown_service.get(name, repo):
                markdown_service.delete(name, repo)
                markdown_service.add(name, content, repo)

            if not markdown_service.get(name, repo):
                markdown_service.add(name, content, repo)

    if "requirements" in objects:
        update_requirements(objects["requirements"])

    if "messages" in objects:
        for m in objects["messages"]:
            message = Message(
                id=m["id"],
                title=m["title"],
                subject=m["subject"],
                body=m["body"],
                job=m["job"],
                status=Status(m["status"]),
                date=datetime.fromisoformat(m["date"]),
                files=m.get("files", []),
            )

            if replace:
                if message_service.get(message.id):
                    message_service.delete(message.id)

            message_service.add(message)
