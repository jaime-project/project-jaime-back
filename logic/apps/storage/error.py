from enum import Enum


class StorageError(Enum):
    SERVER_NOT_EXISTS_ERROR = 'SERVER_NOT_EXISTS_ERROR'
    SERVER_ALREADY_EXISTS_ERROR = 'SERVER_ALREADY_EXISTS_ERROR'