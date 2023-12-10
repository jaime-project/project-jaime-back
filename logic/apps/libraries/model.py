from dataclasses import dataclass


@dataclass
class Library():
    name: str
    description: str
    repo: str
    path: str
    branch: str
    user: str = None
    password: str = None

    def __eq__(self, o: object) -> bool:
        return self.name == o.name

    def __dict__(self):
        return {
            'name': self.name,
            'description': self.description,
            'repo': self.repo,
            'user': self.user,
            'path': self.path,
            'branch': self.branch,
            'password': self.password
        }
