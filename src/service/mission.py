from uuid import UUID

from src.adapter.auth import CurrentUser
from src.adapter.leaflet import create_mission_map
from src.domain.models import File, Mission
from src.schemas.map import MissionRequest, MissionResponse
from src.service.uow import UnitOfWork


async def create_mission(
    mission:MissionRequest,
    user: CurrentUser,
    uow: UnitOfWork
):
    # map = create_mission_map(mission.points, mission.date,
    #                          mission.time, mission.drone)

    async with uow:

        file = File(
            title=f"Карта миссии {mission.date}-{mission.time}-{mission.drone}-{user.id}",
            base64_data="map",
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


async def get_all(
        user: CurrentUser,
        uow: UnitOfWork
) -> list[MissionResponse]:
    async with uow:
        missions = await uow.mission.get_list()

        return [MissionResponse(
            mission_time=mission.mission_time,
            description=mission.description,
            map_data=mission.map_data,
            user_last_name=mission.drone.owner.last_name,
            user_first_name=mission.drone.owner.first_name,
            hull_number=mission.drone.hull_number,
            file=mission.file.base64_data,
            file_title=mission.file.title
        ) for mission in missions]
