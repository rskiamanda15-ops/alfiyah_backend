from typing import Optional
import asyncio
import json

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_admin, get_current_user
from app.schemas.booking import BookingCreate, BookingRead, BookingStatusUpdate
from app.services import booking_service
from app.utils.broadcast import broadcaster

router = APIRouter()


@router.get("/stream")
async def stream_bookings(_admin=Depends(get_current_admin)):
    """Defines an SSE endpoint that streams booking updates to clients."""

    async def event_generator():
        queue = await broadcaster.subscribe()
        try:
            while True:
                message = await queue.get()
                # SSE format: data: <json_string>\n\n
                yield f"data: {json.dumps(message)}\n\n"
        except asyncio.CancelledError:
            # This exception is raised when the client disconnects.
            await broadcaster.unsubscribe(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


@router.post("/", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_booking_api(
    payload: BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    return booking_service.create_booking(db=db, payload=payload, user_id=current_user.id)


@router.get("/me", response_model=list[BookingRead])
def list_my_bookings_api(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    order_by: Optional[str] = None,
    segment: Optional[str] = None,
):
    return booking_service.get_user_bookings(db=db, user_id=current_user.id, order_by=order_by, segment=segment)


@router.get("/", response_model=list[BookingRead])
def list_all_bookings_api(
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
    order_by: Optional[str] = None,
    segment: Optional[str] = None,
):
    return booking_service.get_all_bookings(db=db, order_by=order_by, segment=segment)


@router.patch("/{booking_id}", response_model=BookingRead)
def update_booking_status_api(
    booking_id: int,
    payload: BookingStatusUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    return booking_service.update_booking_status(db=db, booking_id=booking_id, payload=payload)