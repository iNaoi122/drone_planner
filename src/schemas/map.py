import datetime

from pydantic import BaseModel


class MissionRequest(BaseModel):

    points: list[dict]
    date: datetime.date
    time: datetime.time
    drone: str
