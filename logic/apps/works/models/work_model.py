from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from multiprocessing import Process


class Status(Enum):
    RUNNING = 'RUNNING'
    TERMINATED = 'TERMINATED'


@dataclass
class WorkStatus():

    id = str
    process: Process
    status: Status
    init_date: datetime
    end_date: datetime

    def __init__(self, thread: Process, id: str, status: Status = Status.RUNNING, init_date: datetime = datetime.now, end_date: datetime = None) -> "WorkStatus":
        self.id = id
        self.process = thread
        self.status = status
        self.init_date = init_date
        self.end_date = end_date

    def finish(self):
        self.end_date = datetime.now()
