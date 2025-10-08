from typing import Annotated

from fastapi import APIRouter, Depends, status

from src.adapter.auth import CurrentUser, get_auth
from src.router.dependencies.uow import get_uow
from src.schemas.models import ResponseModels, RequestModel
from src.service import models
from src.service.uow import UnitOfWork

models_router = APIRouter(prefix="/models")

@models_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_model(
        user: Annotated[CurrentUser, Depends(get_auth())],
        model: RequestModel,
        uow: UnitOfWork = Depends(get_uow),
    ):
    await models.create_model(model=model, uow=uow)
    return


@models_router.get("/")
async def get_all_models(
        user: Annotated[CurrentUser, Depends(get_auth())],
        uow: UnitOfWork = Depends(get_uow),
) -> list[ResponseModels]:
    return await models.get_all_models(uow)


@models_router.get("/{model_id}")
async def get_model(
        model_id:str,
        user: Annotated[CurrentUser, Depends(get_auth())],
        uow: UnitOfWork = Depends(get_uow)
) -> ResponseModels:
    return await models.get_model_by_id(model_id, uow)
