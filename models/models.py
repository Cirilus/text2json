from pydantic import BaseModel
from enum import Enum


class Version(Enum):
    desktop = "desktop"
    mobile = "mobile"


class BusinessTasks(BaseModel):
    tasks: list[str]
    version: Version
