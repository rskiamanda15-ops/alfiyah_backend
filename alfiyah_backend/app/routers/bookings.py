from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_admin, get_current_user
from app.models.service import ServiceType
from app.models.transaction import Transaction
from app.schemas.booking import BookingCreate, BookingRead, BookingStatusUpdate

router = APIRouter()


@router.post("/", response_model=BookingRead, status_code=status.HTTP_201_CREATED)
def create_booking(
    payload: BookingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    service_type = (
        db.query(ServiceType)
        .filter(ServiceType.id == payload.service_type_id)
        .with_for_update()
        .first()
    )
    if not service_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service type not found")
    booking = Transaction(
        user_id=current_user.id,
        service_type_id=service_type.id,
        price_locked=service_type.price,
        status="pending",
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)
    return booking


@router.get("/me", response_model=list[BookingRead])
def list_my_bookings(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    return db.query(Transaction).filter(Transaction.user_id == current_user.id).all()


@router.patch("/{booking_id}", response_model=BookingRead)
def update_booking_status(
    booking_id: int,
    payload: BookingStatusUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    booking = db.query(Transaction).filter(Transaction.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")
    booking.status = payload.status
    db.commit()
    db.refresh(booking)
    return booking
