from decimal import Decimal
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.user import UserRead


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
    priority_score: int
    priority_segment: str
    urgency_level: Optional[str] = None
    monetary_level: Optional[str] = None
    updated_priority_at: Optional[datetime] = None
    user: UserRead # Nested user data

    model_config = {"from_attributes": True}


class BookingStatusUpdate(BaseModel):
    status: str
