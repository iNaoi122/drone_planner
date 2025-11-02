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

class DroneCert(BaseModel):
    title: str
    content: str
    mime_type: str