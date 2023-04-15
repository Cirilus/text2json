from pydantic import BaseModel


class BusinessTasks(BaseModel):
    tasks: list[str]