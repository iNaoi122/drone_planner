import datetime

from pydantic import BaseModel
from uuid import UUID


class MissionRequest(BaseModel):

    points: list[dict]
    date: datetime.date
    time: datetime.time
    drone: str

class MissionResponse(BaseModel):
    id: UUID
    mission_time: datetime.time
    description: str
    map_data: list[dict]
    user_last_name: str
    user_first_name: str
    hull_number: str
    file: str
    file_title: str

