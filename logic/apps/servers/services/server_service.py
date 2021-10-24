
import json
from pathlib import Path
from typing import List

from logic.apps.servers.models.server_model import Server

_JSON_SERVER_FILE = f'{Path.home()}/.jaime/servers.json'


def add(server: Server):

    with open(_JSON_SERVER_FILE, 'r') as f:
        servers = json.loads(f.read())

    servers.append({
        "name": server.name,
        "url": server.url,
        "token": server.token,
        "version": server.version
    })

    with open(_JSON_SERVER_FILE, 'w') as f:
        f.write(json.dumps(servers))


def get(name: str) -> Server:

    with open(_JSON_SERVER_FILE, 'r') as f:
        servers = json.loads(f.read())

    for s in servers:
        if s['name'] == name:
            return Server(
                name=s['name'],
                url=s['url'],
                token=s['token'],
                version=s['version']
            )

    return None


def list_all() -> List[Server]:

    with open(_JSON_SERVER_FILE, 'r') as f:
        servers = json.loads(f.read())

    return [
        Server(
            name=s['name'],
            url=s['url'],
            token=s['token'],
            version=s['version']
        )
        for s in servers
    ]


def delete(name: str):

    with open(_JSON_SERVER_FILE, 'r') as f:
        servers = json.loads(f.read())

    servers_new = [
        s for s in servers
        if s.name != name
    ]

    with open(_JSON_SERVER_FILE, 'w') as f:
        f.write(json.dumps(servers_new))


def get_path() -> str:

    global _JSON_SERVER_FILE
    return _JSON_SERVER_FILE
