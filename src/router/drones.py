import base64
import json
from typing import Annotated

from fastapi import APIRouter, Depends, UploadFile, File, status, Form, \
    HTTPException, Response
from pydantic import ValidationError

from src.adapter.auth import CurrentUser, get_auth
from src.router.dependencies.uow import get_uow
from src.schemas.drones import ResponseDrone, CreateDrone
from src.service import drones
from src.service.drones import load_drone_cert
from src.service.uow import UnitOfWork

drones_router = APIRouter(prefix="/drones")


@drones_router.get("/")
async def get_all_drones(
    user: Annotated[CurrentUser, Depends(get_auth())],
    uow: UnitOfWork = Depends(get_uow),
) -> list[ResponseDrone]:
    return await drones.get_all_drones(user, uow=uow)


@drones_router.post("/", status_code=status.HTTP_200_OK)
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
    file = await drones.create_drone(user=user, uow=uow, drone=drone, image=image)
    return Response(
            content=base64.b64decode(file.content),
            media_type='application/pdf',
        )


@drones_router.delete("/{drone_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_drone(
    drone_id: str,
    user: Annotated[CurrentUser, Depends(get_auth())],
    uow: UnitOfWork = Depends(get_uow),
):
    await drones.delete_drone(uow, drone_id)
    return


@drones_router.put("/{drone_id}", status_code=status.HTTP_200_OK)
async def update_drone(
    user: Annotated[CurrentUser, Depends(get_auth())],
    drone_id: str,   
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
    file = await drones.update_drone(uow=uow, drone_id=drone_id, image=image, drone=drone)
    return Response(
        content=base64.b64decode(file.content),
        media_type='application/pdf',
    )

@drones_router.get("/{mission_id}/file", status_code=status.HTTP_200_OK)
async def load_drone_cert_by_mission(
    user: Annotated[CurrentUser, Depends(get_auth())],
    mission_id: str,
    uow: UnitOfWork = Depends(get_uow),
    ):
    file = await load_drone_cert(
        uow=uow,
        mission_id=mission_id
    )
    return Response(
        content=base64.b64decode(file.content),
        media_type='application/pdf',
    )

