from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel


class BookingCreate(BaseModel):
    service_type_id: int
    tanggal_acara: datetime
    jumlah_client: int


class BookingRead(BaseModel):
    id: int
    user_id: int
    service_type_id: int
    price_locked: Decimal
    status: str
    tanggal_booking: datetime
    tanggal_acara: datetime
    jumlah_client: int

    model_config = {"from_attributes": True}


class BookingStatusUpdate(BaseModel):
    status: str
