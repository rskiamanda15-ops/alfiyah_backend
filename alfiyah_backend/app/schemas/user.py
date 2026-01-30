from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    model_config = {"from_attributes": True}
