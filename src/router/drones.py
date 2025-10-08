import json
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, status, Form, \
    HTTPException
from pydantic import ValidationError

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
    return await drones.get_all_drones(user, uow=uow)


@drones_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_drone(
    user: Annotated[CurrentUser, Depends(get_auth())],
    drone_data: str = Form(...),
    image: UploadFile = File(...),
    uow: UnitOfWork = Depends(get_uow),

):
    try:
        drone_dict = json.loads(drone_data)
        drone = CreateDrone(**drone_dict)
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON format")
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())
    await drones.create_drone(user=user, uow=uow, drone=drone, image=image)
    return


@drones_router.delete("/{drone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_drone(
    drone_id: str,
    user: Annotated[CurrentUser, Depends(get_auth())],
    uow: UnitOfWork = Depends(get_uow),
):
    await drones.delete_drone(uow, drone_id)
    return


@drones_router.put("/{drone_id", status_code=status.HTTP_204_NO_CONTENT)