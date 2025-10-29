from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from typing import Any


class BaseRepo[T]:

    def __init__(self, session: AsyncSession, model: T):
        self._session = session
        self._model = model

    def add(self, model: T) -> T:
        self._session.add(model)
        return model

    async def get(
        self, field: str, value: Any,
        joined_load: list[str] | None = None
    ) -> T | None:
        q = select(self._model).where(getattr(self._model, field) == value)
        if joined_load:
            q = q.options(*(joinedload(getattr(self._model, field))
                            for field in joined_load))
        return (await self._session.execute(q)).scalars().first()

    async def delete(self, model: T):
        return await self._session.delete(model)

    async def get_or_error(
        self, field: str, value: Any,
        joined_load: list[str] | None = None) -> T:
        if res := await self.get(field=field, value=value,
                                 joined_load=joined_load):
            return res
        raise Exception(f"{self._model.__name__} with field"
                        f" {field} == {value} not found")

    def update(self, model: T):
        self._session.add(model)

    async def get_list(self, field: str | None = None,
                       value: Any | None = None) -> list[T]:
        q = select(self._model)
        if field:
            q = q.where(getattr(self._model, field) == value)
        return (await self._session.execute(q)).scalars().all()