from dataclasses import dataclass


@dataclass
class Repo():

    name: str
    git_path: str
    git_user: str
    git_pass: str
    git_url: str

    def __eq__(self, o: object) -> bool:
        return self.name == o.name

    def __dict__(self):
        return {
            'name': self.name,
            'git_path': self.git_path,
            'git_user': self.git_user,
            'git_pass': self.git_pass,
            'git_url': self.git_url,
        }
