from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class FileList():
    dirs: list[str, object] = field(default_factory=list)
    files: list[str, object] = field(default_factory=list)

    def __dict__(self):
        return {
            'dirs': self.dirs,
            'files': self.files,
        }


@dataclass
class FileDetail():
    name: str
    last_modification: datetime
    creation_date: datetime
    size: str

    def __dict__(self):
        return {
            'name': self.name,
            'last_modification': self.last_modification.isoformat(),
            'creation_date': self.creation_date.isoformat(),
            'size': self.size,
        }
