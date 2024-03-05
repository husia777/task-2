from pydantic import BaseModel


class Assignee(BaseModel):
    username: str
