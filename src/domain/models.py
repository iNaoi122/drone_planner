import uuid

from sqlalchemy import ForeignKey, JSON
from uuid import  UUID
from sqlalchemy.orm import relationship, DeclarativeBase, Mapped, mapped_column
import datetime


class Base(DeclarativeBase):

    id: Mapped[UUID] = mapped_column(default=uuid.uuid4, primary_key=True)
    created_at: Mapped[datetime.datetime] = mapped_column(default=datetime.datetime.utcnow)

    def to_dict(self) -> dict:
        return {
            c.name: str(getattr(self, c.name)) for c in self.__table__.columns
        }

class Role(Base):
    __tablename__ = 'role'

    title: Mapped[str]
    users: Mapped[list['User']] = relationship(back_populates="role")


class User(Base):
    __tablename__ = 'user'

    first_name: Mapped[str]
    middle_name: Mapped[str]
    last_name: Mapped[str]
    login: Mapped[str]
    password: Mapped[str]
    age: Mapped[int]
    role_id: Mapped[UUID] = mapped_column(ForeignKey('role.id'))
    role: Mapped['Role'] = relationship(back_populates='users')
    id_card_series: Mapped[int]
    id_card_number: Mapped[int]

    drones: Mapped[list['Drone']] = relationship(back_populates='owner')


class Model(Base):
    __tablename__ = 'model'

    title: Mapped[str]
    factory: Mapped[str]
    description: Mapped[str]
    weight: Mapped[float]
    max_range: Mapped[float]

    drones: Mapped[list['Drone']] = relationship(back_populates='model')

class File(Base):
    __tablename__ = 'file'

    title: Mapped[str]
    base64_data: Mapped[str]
    mime_type: Mapped[str]

    drones: Mapped[list['Drone']] = relationship(back_populates='file')
    missions: Mapped[list['Mission']] = relationship(back_populates='file')

class Drone(Base):
    __tablename__ = 'drone'

    model_id: Mapped[UUID] = mapped_column(ForeignKey('model.id'))
    model: Mapped['Model'] = relationship(back_populates='drones')
    title: Mapped[str]
    description: Mapped[str | None]
    hull_number: Mapped[str]
    file_id: Mapped[UUID] = mapped_column(ForeignKey('file.id'))
    file: Mapped['File'] = relationship(back_populates='drones')

    owner_id: Mapped[UUID] = mapped_column(ForeignKey('user.id'))
    owner: Mapped['User'] = relationship(back_populates='drones')
    is_deleted: Mapped[bool]
    missions: Mapped[list['Mission']] = relationship(back_populates='drone')

class Mission(Base):
    __tablename__ = 'mission'

    drone_id: Mapped[UUID] = mapped_column(ForeignKey('drone.id'))
    drone: Mapped['Drone'] = relationship(back_populates='missions')

    file_id: Mapped[UUID] = mapped_column(ForeignKey('file.id'))
    file: Mapped['File'] = relationship(back_populates='missions')

    mission_time: Mapped[datetime.time]
    description: Mapped[str]
    map_data: Mapped[dict] = mapped_column(JSON())