from enum import Enum


class BugType(Enum):
    MISSING = 1


class BugLocation(Enum):
    MONSTERS = 1


class BugStatus(Enum):
    OPEN = 1
