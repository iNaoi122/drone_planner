import uuid

from fastapi import UploadFile

from src.adapter.auth import CurrentUser
from src.domain.models import Model, User, Drone
from src.schemas.drones import ResponseDrone, CreateDrone
from src.service.uow import UnitOfWork


async def get_all_drones(user: CurrentUser) -> list[ResponseDrone]:
    if user.role == "user":
        return [
            ResponseDrone(id=uuid.uuid4(), title="MAVIC 3T"),
            ResponseDrone(id=uuid.uuid4(), title="AVATA")
        ]
    return [
            ResponseDrone(id=uuid.uuid4(), title="MAVIC 3T"),
            ResponseDrone(id=uuid.uuid4(), title="AVATA"),
            ResponseDrone(id=uuid.uuid4(), title="Герань")
        ]



async def create_drone(
        user: CurrentUser,
        uow: UnitOfWork,
        drone: CreateDrone,
        image: UploadFile
    ):
    async with uow:
        uow.add(Drone)


