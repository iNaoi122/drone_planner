import base64
import os
import string
import tempfile
import random
import uuid

from fastapi import UploadFile

from src.adapter.auth import CurrentUser
# from src.adapter.cert import generate_drone_cert_base64
from src.domain.models import Drone, File
from src.schemas.drones import ResponseDrone, CreateDrone
from src.service.uow import UnitOfWork


async def get_all_drones(user: CurrentUser, uow:UnitOfWork) -> list[ResponseDrone]:
    if user.role == "user":
        drones = await uow.drone.get_list("owner_id", user.id)
    else:
        drones = await uow.drone.get_list()
    return [ResponseDrone(
            id=drone.id,
            title=drone.title,
            model_id=drone.model_id,
            hull_number=drone.hull_number,
            description=drone.description,
            photo=base64.b64encode(drone.photo).decode("utf-8")
        ) for drone in drones]



async def create_drone(
    user: CurrentUser,
    uow: UnitOfWork,
    drone: CreateDrone,
    image: UploadFile
):
    async with uow:
        user = await uow.user.get("id", user.id)
        hull_number = generate_flight_number()
        temp_file = None
        try:
            content = await image.read()
            with tempfile.NamedTemporaryFile(delete=False) as tmp:
                tmp.write(content)
                temp_file = tmp.name

            # base64_pdf = generate_drone_cert_base64(
            #     image=temp_file,
            #     hull_number=hull_number,
            #     owner=user.last_name+" "+user.first_name
            # )
            base64_pdf = "djlsfs"

        finally:
            if temp_file and os.path.exists(temp_file):
                os.unlink(temp_file)

        file_obj = File(
            title=f"drone_certificate_{hull_number}.pdf",
            base64_data=base64_pdf,
            mime_type="application/pdf"
        )

        drone_obj = Drone(
            model_id=drone.model_id,
            title=drone.title,
            description=drone.description,
            hull_number=hull_number,
            file=file_obj,
            photo=content,
            owner_id=user.id,
            is_deleted=False
        )

        uow.add(drone_obj)
        await uow.commit()



async def delete_drone(
    uow: UnitOfWork,
    drone_id: str,
):
    async with uow:
        drone = await uow.drone.get_or_error("id", drone_id)
        drone.is_deleted = True
        uow.drone.update(drone)
        await uow.commit()


def generate_flight_number():
    prefix = "RU-"
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return prefix + random_part