from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File

from src.adapter.auth import CurrentUser, get_auth
from src.schemas.drones import ResponseDrone, CreateDrone
from src.service import  drones

drones_router = APIRouter(prefix="/drones")

@drones_router.get("/")
async def get_all_drones(
        user: Annotated[CurrentUser, Depends(get_auth())]
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



