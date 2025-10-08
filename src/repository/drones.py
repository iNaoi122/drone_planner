from typing import Any

from sqlalchemy import select

from src.repository.base import BaseRepo


class DroneRepo[T](BaseRepo):

    async def get_list(self, field: str | None = None,
                       value: Any | None = None, for_user: bool = True) -> list[T]:
        q = select(self._model)
        if field:
            q = q.where(getattr(self._model, field) == value)
        if for_user:
            q = q.filter(self._model.is_deleted.is_(False))
        return (await self._session.execute(q)).scalars().all()