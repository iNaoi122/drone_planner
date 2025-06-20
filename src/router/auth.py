from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.adapter.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token, Token
from src.router.dependencies.uow import get_uow
from src.service.uow import UnitOfWork

auth_router = APIRouter()


@auth_router.post("/login")
async def login():
    return


@auth_router.post("/reg")
async def reg():
    return


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


