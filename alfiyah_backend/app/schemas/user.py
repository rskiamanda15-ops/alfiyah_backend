from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)
    address: str | None = Field(default=None, max_length=255)
    phone_number: str | None = Field(default=None, max_length=20)


class UserRead(BaseModel):
    id: int
    name: str
    email: EmailStr
    address: str | None = None
    phone_number: str | None = None
    role: str

    model_config = {"from_attributes": True}


from typing import Optional

class UserUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=100)
    email: Optional[EmailStr] = None
    address: Optional[str] = Field(None, max_length=255)
    phone_number: Optional[str] = Field(None, max_length=20)

