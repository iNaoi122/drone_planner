from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.adapter.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, \
    Token, pwd_context, CurrentUser, get_auth
from src.domain.models import User
from src.router.dependencies.uow import get_uow
from src.schemas.user import RegisterRequest, RegisterResponse
from src.service.uow import UnitOfWork

auth_router = APIRouter()


@auth_router.get("/user-info")
async def user_info(
        user: CurrentUser = Depends(get_auth()),
        uow: UnitOfWork = Depends(get_uow),
) -> RegisterResponse :
    async with uow:
        db_user = await uow.user.get_or_error("id", user.id, ["role"])
        r = RegisterResponse(
            first_name=db_user.first_name,
            middle_name=db_user.middle_name,
            last_name=db_user.last_name,
            role=db_user.role.title
        )
    return r

@auth_router.post("/reg", status_code=status.HTTP_201_CREATED)
async def reg(
    user: RegisterRequest,
    uow: UnitOfWork = Depends(get_uow)
):

    async with uow:

        role = await uow.role.get("title", "user")
        new_user = User(
            first_name=user.first_name,
            middle_name=user.middle_name,
            last_name=user.last_name,
            login=user.login,
            password=pwd_context.hash(user.password),
            birth_date=user.birth_date,
            role=role,
            id_card_series=user.id_card_series,
            id_card_number=user.id_card_number
        )
        uow.add(new_user)
        await uow.commit()

@auth_router.post("/token", response_model=Token)
async def token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        uow: UnitOfWork = Depends(get_uow)
):
    async with uow:
        user = await uow.user.get(field="login", value=form_data.username,
                                  joined_load=['role'])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"user_id": str(user.id), "role": user.role.title},
            expires_delta=access_token_expires
        )
        return {"access_token": access_token, "token_type": "bearer"}


