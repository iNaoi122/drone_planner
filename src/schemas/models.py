from pydantic import  BaseModel
from uuid import UUID


class ResponseModels(BaseModel):

    id: UUID
    title: str
    weight: float
    max_range: float
    description: str


class RequestModel(BaseModel):

    title: str
    weight: float
    range: float
    description: str
    factory: str