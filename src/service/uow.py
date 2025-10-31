import asyncio

from sqlalchemy.ext.asyncio import AsyncSession

from src.repository.base import BaseRepo
from src.repository.mission import MissionRepo
from src.repository.drones import DroneRepo
from src.domain.models import User, Model, Mission, File, Drone, Role

class UnitOfWork:

    def __init__(self, session_factory):
        self._session_factory = session_factory

    async def __aenter__(self):
        self._session: AsyncSession= self._session_factory()

        self._user = BaseRepo[User](session=self._session, model=User)
        self._model = BaseRepo[Model](session=self._session, model=Model)
        self._mission = MissionRepo[Mission](session=self._session, model=Mission)
        self._file = BaseRepo[File](session=self._session, model=File)
        self._drone = DroneRepo[Drone](session=self._session, model=Drone)
        self._role = BaseRepo[Role](session=self._session, model=Role)
        return

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self._session.expunge_all()
        asyncio.shield(self._session.close())
        self._session = None

    async def commit(self):
        await self._session.commit()

    async def rollback(self):
        await self._session.rollback()

    async def refresh(self, model):
        await self._session.refresh(model)

    @property
    def user(self):
        return self._user

    @property
    def file(self):
        return self._file

    @property
    def drone(self):
        return self._drone

    @property
    def model(self):
        return self._model

    @property
    def mission(self):
        return self._mission

    @property
    def role(self):
        return self._role

    def add(self, model):
        self._session.add(model)