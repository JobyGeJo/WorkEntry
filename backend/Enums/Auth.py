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

class Roles(Enum):
    ADMIN = "Admin"
    MANAGER = "Manager"
    FINANCE = "Finance"
    EMPLOYEE = "Employee"
    USER = "User"

class Permissions(Enum):
    POST = 1
    GET = 2
    PUT = 4
    PATCH = 4
    DELETE = 8
    ALL = 15