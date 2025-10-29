from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.domain.models import Mission, Drone
from src.repository.base import BaseRepo

class MissionRepo[T](BaseRepo):

    async def get_list(self, field: str | None = None,
                       value: Any | None = None) -> list[T]:
        query = (
            select(Mission)
            .options(
                joinedload(Mission.drone).options(
                    joinedload(Drone.model),
                    joinedload(Drone.file),
                    joinedload(Drone.owner)
                ),
                joinedload(Mission.file)
            )
            .order_by(Mission.created_at.desc())
        )

        result = await self._session.execute(query)
        return result.scalars().all()