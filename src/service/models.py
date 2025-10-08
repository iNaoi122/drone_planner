from src.schemas.models import ResponseModels, RequestModel
from src.service.uow import UnitOfWork
from src.domain.models import Model


async def get_all_models(uow: UnitOfWork) -> list[ResponseModels]:

    async with uow:
        resp = await uow.model.get_list()
        return [ResponseModels(
            id=r.id,
            title=r.title,
            weight=r.weight,
            max_range=r.max_range,
            description=r.description
        ) for r in resp]

async def create_model(
        model: RequestModel,
        uow: UnitOfWork
    ):
    async with uow:

        uow.add(Model(
            title=model.title,
            factory=model.factory,
            description=model.description,
            weight=model.weight,
            max_range=model.range
        ))
        await uow.commit()

    return


async def get_model_by_id(model_id: str, uow:UnitOfWork) -> ResponseModels:

    async with uow:
        model = await uow.model.get_or_error(field='id', value=id)
        return ResponseModels(
            id=model.id,
            title=model.title,
            weight=model.weight,
            max_range=model.max_range,
            description=model.description
        )