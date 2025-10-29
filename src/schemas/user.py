from pydantic import BaseModel


class RegisterRequest(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    login: str
    password: str
    age: int
    id_card_series: int
    id_card_number: int


class RegisterResponse(BaseModel):
    first_name: str
    middle_name: str
    last_name: str
    role: str
