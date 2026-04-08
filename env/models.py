from pydantic import BaseModel
from typing import List

class Resource(BaseModel):
    id: str
    type: str
    config: dict

class Action(BaseModel):
    action: str

class Observation(BaseModel):
    resources: List[Resource]
    issues_found: List[str]
    step_count: int