import base64
from typing import Annotated

from fastapi import APIRouter, Depends, status, Response

from src.adapter.auth import CurrentUser, get_auth
from src.router.dependencies.uow import get_uow
from src.schemas.map import MissionRequest, MissionResponse
from src.service.mission import create_mission, get_all, get_mission_file
from src.service.uow import UnitOfWork

mission_router = APIRouter(prefix="/mission")




@mission_router.post("/save", status_code=status.HTTP_201_CREATED)
async def save_mission(
        mission:MissionRequest,
        user: Annotated[CurrentUser, Depends(get_auth())],
        uow: UnitOfWork = Depends(get_uow),

):
    map_base64 = await create_mission(mission, user, uow)
    return Response(
            content=base64.b64decode(map_base64),
            media_type='application/pdf',
        )


@mission_router.get("/all")
async def get_all_mission(
        user: Annotated[CurrentUser, Depends(get_auth())],
        uow: UnitOfWork = Depends(get_uow)
) -> list[MissionResponse]:
    return await get_all(user, uow)

@mission_router.get("/{mission_id}/file", status_code=status.HTTP_201_CREATED)
async def save_mission(
        user: Annotated[CurrentUser, Depends(get_auth())],
        mission_id: str,
        uow: UnitOfWork = Depends(get_uow),

):
    map_base64 = await get_mission_file(uow, mission_id)
    return Response(
            content=base64.b64decode(map_base64),
            media_type='application/pdf',
        )