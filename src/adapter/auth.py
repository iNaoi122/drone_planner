from datetime import datetime, timedelta
from typing import Callable
from uuid import UUID, uuid4

from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from src.router.dependencies.uow import get_uow
from src.service.uow import UnitOfWork

# Настройки безопасности
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "your-secret-key"  # Замените на случайную строку в продакшене
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class User(BaseModel):
    id: UUID
    username: str
    role: str
    disabled: bool = False


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str = None
    role: str = None


class CurrentUser(BaseModel):
    id: UUID
    role: str


# Имитация базы данных
fake_users_db = {
    "admin": UserInDB(
        id=uuid4(),
        username="admin",
        role="admin",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        # = "secret"
    ),
    "user": UserInDB(
        id=uuid4(),
        username="user",
        role="user",
        hashed_password="$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        # = "secret"
    ),
}


class AuthHandler:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    async def __call__(self,
                       token: str = Depends(oauth2_scheme)) -> CurrentUser:
        self.current_user = await self.get_current_user(token)
        return self.current_user

    async def get_current_user(self, token: str) -> CurrentUser:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id: str = payload.get("user_id")
            role: str = payload.get("role")
            if user_id is None or role is None:
                raise credentials_exception
            token_data = TokenData(user_id=user_id, role=role)
        except JWTError:
            raise credentials_exception

        user = None
        async with self.uow:
            user  = await self.uow.user.get('id', token_data.user_id,
                                                  joined_load=['role'])
            if user is None:
                raise credentials_exception

            return CurrentUser(id=user.id, role=user.role.title)

    def check_roles(self, roles: list[str] | None):
        if self.roles and self.current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )



def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Фабрика для создания зависимостей
def get_auth() -> Callable:
    auth_handler = AuthHandler(get_uow())
    return auth_handler