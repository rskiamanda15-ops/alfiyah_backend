from datetime import datetime
from decimal import Decimal
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.service import ServiceType
from app.models.transaction import Transaction
from app.schemas.booking import BookingCreate, BookingStatusUpdate
from app.utils.priority import calculate_priority


def create_booking(db: Session, payload: BookingCreate, user_id: int):
    service_type = (
        db.query(ServiceType)
        .filter(ServiceType.id == payload.service_type_id)
        .with_for_update()
        .first()
    )
    if not service_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service type not found")

    booking = Transaction(
        user_id=user_id,
        service_type_id=service_type.id,
        price_locked=service_type.price,
        status="pending",
        tanggal_acara=payload.tanggal_acara,
        jumlah_client=payload.jumlah_client,
    )

    # Calculate priority
    result = calculate_priority(booking)
    booking.priority_score = result["priority_score"]
    booking.priority_segment = result["priority_segment"]
    booking.urgency_level = result["urgency_level"]
    booking.monetary_level = result["monetary_level"]
    booking.updated_priority_at = datetime.utcnow()

    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


def get_user_bookings(db: Session, user_id: int, order_by: Optional[str] = None, segment: Optional[str] = None):
    query = db.query(Transaction).options(joinedload(Transaction.user)).filter(Transaction.user_id == user_id)
    if segment:
        query = query.filter(Transaction.priority_segment == segment)
    if order_by == "priority_score_desc":
        query = query.order_by(Transaction.priority_score.desc())
    return query.all()


def get_all_bookings(db: Session, order_by: Optional[str] = None, segment: Optional[str] = None):
    query = db.query(Transaction).options(joinedload(Transaction.user))
    if segment:
        query = query.filter(Transaction.priority_segment == segment)
    if order_by == "priority_score_desc":
        query = query.order_by(Transaction.priority_score.desc())
    return query.all()


def update_booking_status(db: Session, booking_id: int, payload: BookingStatusUpdate):
    booking = db.query(Transaction).filter(Transaction.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    # Update status
    booking.status = payload.status

    # Recalculate priority after status update
    result = calculate_priority(booking)
    booking.priority_score = result["priority_score"]
    booking.priority_segment = result["priority_segment"]
    booking.urgency_level = result["urgency_level"]
    booking.monetary_level = result["monetary_level"]
    booking.updated_priority_at = datetime.utcnow()

    db.commit()
    db.refresh(booking)
    return booking
