from enum import Enum


class ClusterError(Enum):
    CLUSTER_NOT_EXISTS_ERROR = 'CLUSTER_NOT_EXISTS_ERROR'
    CLUSTER_ALREADY_EXISTS_ERROR = 'CLUSTER_ALREADY_EXISTS_ERROR'
