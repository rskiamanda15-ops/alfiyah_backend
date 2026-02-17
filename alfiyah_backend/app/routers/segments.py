from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_admin
from app.schemas.segment import SegmentItem
from app.services.segmentation import segment_customers

router = APIRouter()


@router.get("/", response_model=list[SegmentItem])
def list_segments(db: Session = Depends(get_db), _admin=Depends(get_current_admin)):
    try:
        results = segment_customers(db, k=4)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return [
        SegmentItem(
            user_id=point.user_id,
            name=point.name,
            recency=point.recency,
            frequency=point.frequency,
            monetary=point.monetary,
            cluster=label,
            customer_segment=segment_label,
        )
        for point, label, segment_label in results
    ]
