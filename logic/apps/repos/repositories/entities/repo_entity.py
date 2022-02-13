from logic.apps.repos.models.repo_model import RepoGit, Repo
from logic.libs.sqliteAlchemy import sqliteAlchemy
from sqlalchemy import Column, String

Entity = sqliteAlchemy.get_entity_class()


class RepoGitEntity(Entity):
    __tablename__ = 'REPOSITORIES_GIT'

    name = Column(String, primary_key=True, nullable=False)
    git_path = Column(String)
    git_user = Column(String)
    git_pass = Column(String)
    git_url = Column(String)

    def to_model(self) -> RepoGit:
        return RepoGit(
            name=self.name,
            git_path=self.git_path,
            git_user=self.git_user,
            git_pass=self.git_pass,
            git_url=self.git_url
        )

    @staticmethod
    def from_model(m: RepoGit) -> 'RepoGitEntity':
        return RepoGitEntity(
            name=m.name,
            git_path=m.git_path,
            git_user=m.git_user,
            git_pass=m.git_pass,
            git_url=m.git_url
        )


class RepoLocalEntity(Entity):
    __tablename__ = 'REPOSITORIES_LOCAL'

    name = Column(String, primary_key=True, nullable=False)

    def to_model(self) -> Repo:
        return Repo(
            name=self.name
        )

    @staticmethod
    def from_model(m: Repo) -> 'RepoLocalEntity':
        return RepoGitEntity(
            name=m.name
        )
