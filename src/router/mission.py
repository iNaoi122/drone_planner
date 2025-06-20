from typing import Annotated

from fastapi import APIRouter, Depends

from src.adapter.auth import CurrentUser, get_auth
from src.schemas.map import MissionRequest
from src.adapter.leaflet import create_mission_map

mission_router = APIRouter(prefix="/mission")




@mission_router.post("/save")
async def save_mission(
        mission:MissionRequest,
        user: Annotated[CurrentUser, Depends(get_auth())]
):
    map = create_mission_map(mission.points, mission.date,
                       mission.time, mission.drone)



@mission_router.get("/all")
async def get_all_mission(
        user: Annotated[CurrentUser, Depends(get_auth())]

):
    return