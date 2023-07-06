from abc import ABC
from dataclasses import dataclass

from http_rest_client.command_dispatch import Dispatch


class Command(ABC):
    pass


@dataclass
class Auth0Command(Command):
    client_id: str
    client_secret: str
    audience: str
    grant_type: str


class Auth0CommandHandler:
    def execute(self, command: Auth0Command):
        pass


Dispatch().register(Auth0Command, Auth0CommandHandler())
