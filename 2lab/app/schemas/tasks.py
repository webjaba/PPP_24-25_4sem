from pydantic import BaseModel, HttpUrl
from enum import Enum
from typing import Optional


class TaskStatusEnum(str, Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"
    failed = "failed"


class TaskCreate(BaseModel):
    url: HttpUrl
    max_depth: int
    format: str  # "graphml"


class TaskOut(BaseModel):
    id: int
    url: str
    status: TaskStatusEnum
    result: Optional[str] = None

    class Config:
        orm_mode = True
