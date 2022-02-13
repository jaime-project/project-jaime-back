from dataclasses import dataclass
from enum import Enum


class RepoType(Enum):
    GIT = 'GIT'
    LOCAL = 'LOCAL'


@dataclass
class Repo():
    name: str = None
    type: RepoType = RepoType.LOCAL

    def __eq__(self, o: object) -> bool:
        return self.name == o.name

    def __dict__(self):
        return {
            'name': self.name,
            'type': self.type.value
        }


@dataclass
class RepoGit(Repo):

    type: RepoType = RepoType.GIT
    git_path: str = None
    git_user: str = None
    git_pass: str = None
    git_url: str = None

    def __eq__(self, o: object) -> bool:
        return self.name == o.name

    def __dict__(self):
        return {
            'name': self.name,
            'type': self.type.value,
            'git_path': self.git_path,
            'git_user': self.git_user,
            'git_pass': self.git_pass,
            'git_url': self.git_url,
        }
