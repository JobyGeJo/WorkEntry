from enum import Enum


class AuthEvents(Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    TOKEN_EXPIRED = "TOKEN EXPIRED"

class AuthTypes(Enum):
    PASSWORD = "LOGIN"
    SESSION = "SESSION"
    TOKEN = "TOKEN"
    API_KEY = "API_KEY"

class Roles(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

    @property
    def rank(self) -> int:
        """Define ranking for comparison"""
        ranking = {
            Roles.OWNER: 4,
            Roles.ADMIN: 3,
            Roles.MANAGER: 2,
            Roles.USER: 1,
        }
        return ranking[self]

    def __lt__(self, other):
        if isinstance(other, Roles):
            return self.rank < other.rank
        return NotImplemented

    def __gt__(self, other):
        if isinstance(other, Roles):
            return self.rank > other.rank
        return NotImplemented

