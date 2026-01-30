from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel


class BookingCreate(BaseModel):
    service_type_id: int


class BookingRead(BaseModel):
    id: int
    service_type_id: int
    price_locked: Decimal
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class BookingStatusUpdate(BaseModel):
    status: str
