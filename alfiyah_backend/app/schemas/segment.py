from decimal import Decimal
from pydantic import BaseModel


class SegmentItem(BaseModel):
    user_id: int
    name: str
    recency: int
    frequency: int
    monetary: Decimal
    cluster: int

    model_config = {"from_attributes": True}
