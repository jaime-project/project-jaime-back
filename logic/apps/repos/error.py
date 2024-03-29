from enum import Enum


class RepoError(Enum):
    REPO_NOT_EXISTS_ERROR = 'REPO_NOT_EXISTS_ERROR'
    REPO_ALREADY_EXISTS_ERROR = 'REPO_ALREADY_EXISTS_ERROR'
