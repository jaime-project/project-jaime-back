from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from threading import Thread


class Status(Enum):
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'
    RUNNING = 'RUNNING'


@dataclass
class WorkStatus():

    thread: Thread
    status: Status
    init_date: datetime
    end_date: datetime

    def __init__(self, thread: Thread, status: Status = Status.RUNNING, init_date: datetime = datetime.now, end_date: datetime = None) -> "WorkStatus":
        self.thread = thread
        self.status = status
        self.init_date = init_date
        self.end_date = end_date

    def finish(self):
        self.end_date = datetime.now()
