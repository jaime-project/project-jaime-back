import subprocess
from dataclasses import dataclass


@dataclass
class Server():
    name: str
    url: str
    token: str
    version: str

    def __init__(self, name: str, url: str, token: str, version: str) -> "Server":
        self.name = name
        self.url = url
        self.token = token
        self.version = version

    def login(self) -> str:
        short_version = self.version.split(".")[0]

        if short_version == "3":
            cmd = f"{self.binary_name()} login {self.url} --token={self.token}"

        if short_version == "4":
            cmd = f"{self.binary_name()} login --server={self.url} --token={self.token}"

        return subprocess.getoutput(cmd)

    def binary_name(self) -> str:
        short_version = self.version.split(".")[0]

        if short_version == "3":
            return "oc"

        return "oc"
