from fastapi import UploadFile

from src.adapter.auth import CurrentUser
from src.domain.models import Model, User, Drone
from src.schemas.drones import ResponseDrone, CreateDrone
from src.service.uow import UnitOfWork


async def get_all_drones(user: CurrentUser, uow:UnitOfWork) -> list[ResponseDrone]:
    if user.role == "user":
        drones = await uow.drone.get_list("owner_id", user.id)
        return [ResponseDrone.from_orm(drone) for drone in drones]
    drones = await uow.drone.get_list()
    return [ResponseDrone.from_orm(drone) for drone in drones]



async def create_drone(
    user: CurrentUser,
    uow: UnitOfWork,
    drone: CreateDrone,
    image: UploadFile
):
    async with uow:
        uow.add(Drone)
