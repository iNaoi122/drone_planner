from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.adapter.auth import CurrentUser, get_auth
from src.router.dependencies.uow import get_uow
from src.schemas.map import MissionRequest, MissionResponse
from src.service.mission import create_mission, get_all
from src.service.uow import UnitOfWork

mission_router = APIRouter(prefix="/mission")




@mission_router.post("/save", status_code=status.HTTP_201_CREATED)
async def save_mission(
        mission:MissionRequest,
        user: Annotated[CurrentUser, Depends(get_auth())],
        uow: UnitOfWork = Depends(get_uow),

):
    await create_mission(mission, user, uow)
    return


@mission_router.get("/all")
async def get_all_mission(
        user: Annotated[CurrentUser, Depends(get_auth())],
        uow: UnitOfWork = Depends(get_uow)
) -> list[MissionResponse]:
    return await get_all(user, uow)