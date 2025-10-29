from uuid import UUID

from pydantic import  BaseModel


class ResponseDrone(BaseModel):
    id: UUID
    title: str
    model_id: UUID
    hull_number: str
    description: str
    photo: str

class CreateDrone(BaseModel):
    model_id: UUID
    title: str
    description: str
