from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File

from src.adapter.auth import CurrentUser, get_auth
from src.router.dependencies.uow import get_uow
from src.schemas.drones import ResponseDrone, CreateDrone
from src.service import drones
from src.service.uow import UnitOfWork

drones_router = APIRouter(prefix="/drones")


@drones_router.get("/")
async def get_all_drones(
    user: Annotated[CurrentUser, Depends(get_auth())],
    uow: UnitOfWork = Depends(get_uow),
) -> list[ResponseDrone]:
    return await drones.get_all_drones(user)


@drones_router.post("/")
async def create_drone(
    drone: CreateDrone,
    user: Annotated[CurrentUser, Depends(get_auth())],
    image: UploadFile = File(...)
):
    return


@drones_router.delete("/")
async def delete_drone(
    user: Annotated[CurrentUser, Depends(get_auth())]
):
    return
