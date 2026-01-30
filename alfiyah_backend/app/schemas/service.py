from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class PackageCreate(BaseModel):
    name: str = Field(..., max_length=120)
    description: Optional[str] = None


class ServiceTypeCreate(BaseModel):
    package_id: int
    name: str = Field(..., max_length=120)
    description: Optional[str] = None
    price: Decimal


class ServiceTypeRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: Decimal

    model_config = {"from_attributes": True}


class PackageRead(BaseModel):
    id: int
    name: str
    description: Optional[str]
    service_types: List[ServiceTypeRead] = []

    model_config = {"from_attributes": True}
