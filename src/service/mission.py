from uuid import UUID

from src.adapter.auth import CurrentUser
from src.adapter.maps import create_mission_pdf_plotly
from src.domain.models import File, Mission
from src.schemas.map import MissionRequest, MissionResponse
from src.service.uow import UnitOfWork


async def create_mission(
    mission:MissionRequest,
    user: CurrentUser,
    uow: UnitOfWork
):

    async with uow:
        drone = await uow.drone.get("id", mission.drone)
        user = await uow.user.get_or_error("id", user.id)
        map_html = create_mission_pdf_plotly(mission.points, mission.date,
                                      mission.time, drone.hull_number,
                                      f"{user.last_name} {user.first_name}",
                                      user.id_card_number
                                    )
        file = File(
            title=f"{mission.date}-{mission.time}-{mission.drone}-{user.last_name} {user.first_name}",
            base64_data=map_html,
            mime_type="application/pdf"
        )

        mission = Mission(
            drone_id=UUID(mission.drone),
            file=file,
            mission_time=mission.time,
            map_data=mission.points,
            description="desc"
        )

        uow.add(mission)

        await uow.commit()
        return map_html


async def get_all(
        user: CurrentUser,
        uow: UnitOfWork
) -> list[MissionResponse]:
    async with uow:
        missions = await uow.mission.get_list()

        return [MissionResponse(
            id=str(mission.id),
            mission_time=mission.mission_time,
            description=mission.description,
            map_data=mission.map_data,
            user_last_name=mission.drone.owner.last_name,
            user_first_name=mission.drone.owner.first_name,
            hull_number=mission.drone.hull_number,
            file=mission.file.base64_data,
            file_title=mission.file.title
        ) for mission in missions]


async def get_mission_file(
    uow: UnitOfWork,
    mission_id: str
    ):
    async with uow:
        mission = await uow.mission.get("id", mission_id)
        file = await uow.file.get("id", mission.file_id)
        return file.base64_data