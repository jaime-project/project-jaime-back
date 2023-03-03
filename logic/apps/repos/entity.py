from sqlalchemy import Column, String, Text

from logic.apps.repos.model import Repo, RepoGit, RepoType
from logic.libs.sqliteAlchemy import sqliteAlchemy

Entity = sqliteAlchemy.get_entity_class()


class RepoGitEntity(Entity):
    __tablename__ = 'REPOSITORIES_GIT'

    name = Column(String(60), primary_key=True, nullable=False)
    git_path = Column(Text)
    git_user = Column(Text)
    git_pass = Column(Text)
    git_branch = Column(String(60))
    git_url = Column(Text)

    def to_model(self) -> RepoGit:
        return RepoGit(
            name=self.name,
            type=RepoType.GIT,
            git_path=self.git_path,
            git_user=self.git_user,
            git_pass=self.git_pass,
            git_branch=self.git_branch,
            git_url=self.git_url
        )

    @staticmethod
    def from_model(m: RepoGit) -> 'RepoGitEntity':
        return RepoGitEntity(
            name=m.name,
            git_path=m.git_path,
            git_user=m.git_user,
            git_pass=m.git_pass,
            git_branch=m.git_branch,
            git_url=m.git_url
        )


class RepoLocalEntity(Entity):
    __tablename__ = 'REPOSITORIES_LOCAL'

    name = Column(String(255), primary_key=True, nullable=False)

    def to_model(self) -> Repo:
        return Repo(
            name=self.name,
            type=RepoType.LOCAL
        )

    @staticmethod
    def from_model(m: Repo) -> 'RepoLocalEntity':
        return RepoLocalEntity(
            name=m.name
        )
