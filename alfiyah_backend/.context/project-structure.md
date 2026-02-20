# Project structure overview
```
// Structure of documents
└── app/
    └── __init__.py
    └── core/
        ├── __init__.py
        ├── config.py
        ├── database.py
        ├── security.py
    └── main.py
    └── models/
        ├── __init__.py
        ├── service.py
        ├── transaction.py
        ├── user.py
    └── routers/
        ├── __init__.py
        ├── auth.py
        ├── bookings.py
        ├── segments.py
        ├── services.py
    └── schemas/
        ├── __init__.py
        ├── auth.py
        ├── booking.py
        ├── segment.py
        ├── service.py
        ├── user.py
    └── services/
        ├── __init__.py
        ├── booking_service.py
        ├── segmentation.py
        ├── user_service.py
    └── utils/
        └── broadcast.py
        └── priority.py

```
###  Path: `/app/__init__.py`

```py

```
###  Path: `/app/core/__init__.py`

```py

```
###  Path: `/app/core/config.py`

```py
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "mysql+pymysql://root@localhost/alfiyah_db"
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    model_config = SettingsConfigDict(
        env_prefix="",
        case_sensitive=False,
    )


settings = Settings()

```
###  Path: `/app/core/database.py`

```py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from app.core.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

```
###  Path: `/app/core/security.py`

```py
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: Optional[int] = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError as exc:
        raise credentials_exception from exc
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception
    return user


def get_current_admin(current_user: User = Depends(get_current_user)) -> User:
    if current_user.role != "admin":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admin access required")
    return current_user

```
###  Path: `/app/main.py`

```py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers import auth, services, bookings, segments

app = FastAPI(title="Alfiyah Booking API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(services.router, prefix="/services", tags=["services"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])
app.include_router(segments.router, prefix="/segments", tags=["segments"])


@app.get("/health")
def health_check():
    return {"status": "ok"}

```
###  Path: `/app/models/__init__.py`

```py
"""SQLAlchemy model registry."""

from app.models.user import User
from app.models.service import Package, ServiceType
from app.models.transaction import Transaction

__all__ = ["User", "Package", "ServiceType", "Transaction"]

```
###  Path: `/app/models/service.py`

```py
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Numeric
from sqlalchemy.orm import relationship

from app.core.database import Base


class Package(Base):
    __tablename__ = "packages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False)
    description = Column(Text)

    service_types = relationship("ServiceType", back_populates="package", cascade="all, delete-orphan")


class ServiceType(Base):
    __tablename__ = "service_types"

    id = Column(Integer, primary_key=True, index=True)
    package_id = Column(Integer, ForeignKey("packages.id"), nullable=False)
    name = Column(String(120), nullable=False)
    description = Column(Text)
    price = Column(Numeric(12, 2), nullable=False)

    package = relationship("Package", back_populates="service_types")
    transactions = relationship("Transaction", back_populates="service_type")

```
###  Path: `/app/models/transaction.py`

```py
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Numeric, String, DateTime
from sqlalchemy.orm import relationship

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    service_type_id = Column(Integer, ForeignKey("service_types.id"), nullable=False)
    price_locked = Column(Numeric(12, 2), nullable=False)
    status = Column(String(20), default="pending", nullable=False)
    tanggal_booking = Column(DateTime, default=datetime.utcnow, nullable=False)
    tanggal_acara = Column(DateTime, nullable=False)
    jumlah_client = Column(Integer, nullable=False)

    user = relationship("User", back_populates="transactions")
    service_type = relationship("ServiceType", back_populates="transactions")

    priority_score = Column(Integer, default=0, nullable=False)
    priority_segment = Column(String(50), default="low", nullable=False)
    urgency_level = Column(String(50))
    monetary_level = Column(String(50))
    updated_priority_at = Column(DateTime)

```
###  Path: `/app/models/user.py`

```py
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    address = Column(String(255))
    phone_number = Column(String(20))
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(20), default="customer", nullable=False)

    transactions = relationship("Transaction", back_populates="user")

```
###  Path: `/app/routers/__init__.py`

```py

```
###  Path: `/app/routers/auth.py`

```py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import create_access_token, get_current_user, get_password_hash, verify_password
from app.models.user import User
from app.schemas.auth import Token
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.services import user_service

router = APIRouter()


@router.post("/register", response_model=UserRead)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    user = User(
        name=user_in.name,
        email=user_in.email,
        address=user_in.address,
        phone_number=user_in.phone_number, # Tambahkan baris ini
        hashed_password=get_password_hash(user_in.password),
        role="customer",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    access_token = create_access_token({"sub": str(user.id)})
    return Token(access_token=access_token)


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UserRead)
def update_current_user(
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return user_service.update_user(db=db, current_user=current_user, user_update=user_update)

```
###  Path: `/app/routers/bookings.py`

```py
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
```
###  Path: `/app/routers/segments.py`

```py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse # New import
from sqlalchemy.orm import Session
import asyncio # New import
import json # New import

from app.core.database import get_db
from app.core.security import get_current_admin
from app.schemas.segment import SegmentItem
from app.services.segmentation import segment_customers, _broadcast_segments # Corrected import

router = APIRouter()


@router.get("/stream")
async def stream_segments(db: Session = Depends(get_db), _admin=Depends(get_current_admin)):
    """Defines an SSE endpoint that streams segment updates to clients."""

    async def event_generator():
        # Broadcast initial segments when a client connects
        try:
            _broadcast_segments(db) # Send current segments immediately
        except Exception as e:
            # Handle error if initial broadcast fails, but don't break the stream
            print(f"Error broadcasting initial segments: {e}")

        queue = await broadcaster.subscribe()
        try:
            while True:
                message = await queue.get()
                # Only send segment updates through this stream
                if message.get("type") == "segment_updated":
                    yield f"data: {json.dumps(message)}\n\n"
        except asyncio.CancelledError:
            await broadcaster.unsubscribe(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")


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

```
###  Path: `/app/routers/services.py`

```py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload # Add joinedload for eager loading

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.service import Package, ServiceType
from app.schemas.service import PackageCreate, PackageRead, ServiceTypeCreate, PackageUpdate, ServiceTypeUpdate # New imports

router = APIRouter()


@router.get("/packages", response_model=list[PackageRead])
def list_packages(db: Session = Depends(get_db)):
    return db.query(Package).options(joinedload(Package.service_types)).all()


@router.post("/packages", response_model=PackageRead, status_code=status.HTTP_201_CREATED)
def create_package(
    payload: PackageCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    existing = db.query(Package).filter(Package.name == payload.name).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Package already exists")
    package = Package(name=payload.name, description=payload.description)
    db.add(package)
    db.commit()
    db.refresh(package)
    # Ensure service_types is loaded for the response
    package_read = db.query(Package).options(joinedload(Package.service_types)).filter(Package.id == package.id).first()
    return package_read


@router.patch("/packages/{package_id}", response_model=PackageRead)
def update_package(
    package_id: int,
    payload: PackageUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    package = db.query(Package).filter(Package.id == package_id).first()
    if not package:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")

    # Update fields from payload
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(package, field, value)

    db.add(package)
    db.commit()
    db.refresh(package)
    # Ensure service_types is loaded for the response
    package_read = db.query(Package).options(joinedload(Package.service_types)).filter(Package.id == package.id).first()
    return package_read


@router.delete("/packages/{package_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_package(
    package_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    package = db.query(Package).filter(Package.id == package_id).first()
    if not package:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")

    db.delete(package)
    db.commit()
    return {"message": "Package deleted successfully"}


@router.post("/types", response_model=PackageRead, status_code=status.HTTP_201_CREATED)
def create_service_type(
    payload: ServiceTypeCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    package = db.query(Package).filter(Package.id == payload.package_id).options(joinedload(Package.service_types)).first()
    if not package:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Package not found")
    service_type = ServiceType(
        package_id=payload.package_id,
        name=payload.name,
        description=payload.description,
        price=payload.price,
    )
    db.add(service_type)
    db.commit()
    db.refresh(service_type) # Refresh service_type to get its ID
    db.refresh(package) # Refresh package to load the newly added service_type
    # Ensure service_types is loaded for the response
    package_read = db.query(Package).options(joinedload(Package.service_types)).filter(Package.id == package.id).first()
    return package_read


@router.patch("/types/{service_type_id}", response_model=PackageRead)
def update_service_type(
    service_type_id: int,
    payload: ServiceTypeUpdate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    service_type = db.query(ServiceType).filter(ServiceType.id == service_type_id).first()
    if not service_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service type not found")

    # Update fields from payload
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(service_type, field, value)

    db.add(service_type)
    db.commit()
    db.refresh(service_type) # Refresh service_type to get its updated values

    # Fetch and return the parent package with updated service types
    package = db.query(Package).options(joinedload(Package.service_types)).filter(Package.id == service_type.package_id).first()
    if not package:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent package not found after service type update")
    return package


@router.delete("/types/{service_type_id}", response_model=PackageRead)
def delete_service_type(
    service_type_id: int,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    service_type = db.query(ServiceType).filter(ServiceType.id == service_type_id).first()
    if not service_type:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service type not found")

    package_id = service_type.package_id # Store package_id before deletion
    db.delete(service_type)
    db.commit()

    # Fetch and return the parent package with updated service types
    package = db.query(Package).options(joinedload(Package.service_types)).filter(Package.id == package_id).first()
    if not package:
        # This case implies the parent package was also deleted, which shouldn't happen
        # if cascade is correctly configured, but handle defensively.
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Parent package not found after service type deletion")
    return package

```
###  Path: `/app/schemas/__init__.py`

```py

```
###  Path: `/app/schemas/auth.py`

```py
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

```
###  Path: `/app/schemas/booking.py`

```py
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

```
###  Path: `/app/schemas/segment.py`

```py
from decimal import Decimal
from pydantic import BaseModel


class SegmentItem(BaseModel):
    user_id: int
    name: str
    recency: int
    frequency: int
    monetary: Decimal
    cluster: int
    customer_segment: str

    model_config = {"from_attributes": True}

```
###  Path: `/app/schemas/service.py`

```py
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


class PackageCreate(BaseModel):
    name: str = Field(..., max_length=120)
    description: Optional[str] = None


class PackageUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=120)
    description: Optional[str] = None


class ServiceTypeCreate(BaseModel):
    package_id: int
    name: str = Field(..., max_length=120)
    description: Optional[str] = None
    price: Decimal


class ServiceTypeUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=120)
    description: Optional[str] = None
    price: Optional[Decimal] = None


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

```
###  Path: `/app/schemas/user.py`

```py
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


```
###  Path: `/app/services/__init__.py`

```py

```
###  Path: `/app/services/booking_service.py`

```py
from datetime import datetime
from decimal import Decimal
from typing import Optional

import anyio
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.models.service import ServiceType
from app.models.transaction import Transaction
from app.schemas.booking import BookingCreate, BookingRead, BookingStatusUpdate
from app.utils.broadcast import broadcaster
from app.utils.priority import calculate_priority
from app.services.segmentation import _broadcast_segments # Modified import


def create_booking(db: Session, payload: BookingCreate, user_id: int):
    service_type = (
        db.query(ServiceType).filter(ServiceType.id == payload.service_type_id).with_for_update().first()
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

    booking_with_user = (
        db.query(Transaction).options(joinedload(Transaction.user)).filter(Transaction.id == booking.id).first()
    )

    if booking_with_user:
        try:
            booking_data = BookingRead.from_orm(booking_with_user).model_dump(mode="json")
            anyio.from_thread.run(broadcaster.broadcast, {"type": "booking_created", "data": booking_data})
        except Exception:
            pass

    _broadcast_segments(db) # Broadcast segments after booking creation

    return booking_with_user


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
    booking = (
        db.query(Transaction).options(joinedload(Transaction.user)).filter(Transaction.id == booking_id).first()
    )
    if not booking:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Booking not found")

    booking.status = payload.status

    result = calculate_priority(booking)
    booking.priority_score = result["priority_score"]
    booking.priority_segment = result["priority_segment"]
    booking.urgency_level = result["urgency_level"]
    booking.monetary_level = result["monetary_level"]
    booking.updated_priority_at = datetime.utcnow()

    db.commit()
    db.refresh(booking)

    try:
        booking_data = BookingRead.from_orm(booking).model_dump(mode="json")
        anyio.from_thread.run(broadcaster.broadcast, {"type": "booking_updated", "data": booking_data})
    except Exception:
        pass

    _broadcast_segments(db) # Broadcast segments after booking update

    return booking

```
###  Path: `/app/services/segmentation.py`

```py
from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Iterable

import anyio # New import
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.segment import SegmentItem # New import
from app.utils.broadcast import broadcaster # New import


@dataclass(frozen=True)
class RfmPoint:
    user_id: int
    name: str
    recency: int
    frequency: int
    monetary: Decimal

    def as_vector(self) -> list[float]:
        return [float(self.recency), float(self.frequency), float(self.monetary)]


def _normalize(points: list[RfmPoint]) -> tuple[list[list[float]], list[float], list[float]]:
    vectors = [p.as_vector() for p in points]
    mins = [min(values) for values in zip(*vectors)]
    maxs = [max(values) for values in zip(*vectors)]
    normalized = []
    for vector in vectors:
        scaled = []
        for value, min_val, max_val in zip(vector, mins, maxs):
            if max_val == min_val:
                scaled.append(0.0)
            else:
                scaled.append((value - min_val) / (max_val - min_val))
        normalized.append(scaled)
    return normalized, mins, maxs


def _euclidean(a: list[float], b: list[float]) -> float:
    return sum((x - y) ** 2 for x, y in zip(a, b)) ** 0.5


def _mean_vector(points: list[list[float]]) -> list[float]:
    if not points:
        return []
    return [sum(values) / len(values) for values in zip(*points)]


def _kmeans(vectors: list[list[float]], k: int, max_iter: int = 100) -> list[int]:
    if k <= 0:
        raise ValueError("k must be positive")
    if len(vectors) < k:
        raise ValueError("k cannot be greater than number of samples")

    random.seed(42)
    centroids = random.sample(vectors, k)
    labels = [0] * len(vectors)

    for _ in range(max_iter):
        new_labels = []
        for vector in vectors:
            distances = [_euclidean(vector, centroid) for centroid in centroids]
            new_labels.append(distances.index(min(distances)))

        if new_labels == labels:
            break
        labels = new_labels

        clusters: list[list[list[float]]] = [[] for _ in range(k)]
        for label, vector in zip(labels, vectors):
            clusters[label].append(vector)

        for idx, cluster in enumerate(clusters):
            if cluster:
                centroids[idx] = _mean_vector(cluster)

    return labels


def build_rfm_points(db: Session) -> list[RfmPoint]:
    latest_booking = func.max(Transaction.tanggal_booking).label("last_booking")
    query = (
        db.query(
            User.id.label("user_id"),
            User.name.label("name"),
            func.count(Transaction.id).label("frequency"),
            func.sum(Transaction.price_locked).label("monetary"),
            latest_booking,
        )
        .join(Transaction, Transaction.user_id == User.id)
        .group_by(User.id, User.name)
    )
    rows = query.all()
    now = datetime.utcnow()
    points: list[RfmPoint] = []
    for row in rows:
        last_booking = row.last_booking
        recency_days = (now - last_booking).days if last_booking else 0
        points.append(
            RfmPoint(
                user_id=row.user_id,
                name=row.name,
                recency=recency_days,
                frequency=int(row.frequency or 0),
                monetary=Decimal(row.monetary or 0),
            )
        )
    return points


def segment_customers(db: Session, k: int) -> list[tuple[RfmPoint, int, str]]:
    points = build_rfm_points(db)
    if not points:
        return []
    vectors, _, _ = _normalize(points)
    labels = _kmeans(vectors, k=k)

    # Group points by cluster
    clusters_data = {i: [] for i in range(k)}
    for point, label in zip(points, labels):
        clusters_data[label].append(point)

    # Calculate average RFM for each cluster
    cluster_metrics = {}
    for cluster_id, cluster_points in clusters_data.items():
        if cluster_points:
            # Ensure Decimal values are converted to float for sum/average if needed, or handle Decimal arithmetic
            avg_recency = sum(p.recency for p in cluster_points) / len(cluster_points)
            avg_frequency = sum(p.frequency for p in cluster_points) / len(cluster_points)
            # Convert Decimal to float for weighted average, or ensure consistent type for comparison
            avg_monetary = float(sum(p.monetary for p in cluster_points)) / len(cluster_points)
            
            cluster_metrics[cluster_id] = {
                "avg_recency": avg_recency,
                "avg_frequency": avg_frequency,
                "avg_monetary": avg_monetary,
                "num_points": len(cluster_points)
            }
        else:
            cluster_metrics[cluster_id] = {
                "avg_recency": 0, "avg_frequency": 0, "avg_monetary": 0, "num_points": 0
            }

    # Determine mapping from cluster ID to segment label
    # Sort clusters based on a "value" metric (e.g., higher frequency and monetary, lower recency)
    # This key defines the "best" cluster. We'll give higher weight to monetary and frequency.
    ranked_clusters = sorted(
        cluster_metrics.items(),
        key=lambda item: (item[1]["avg_frequency"] * item[1]["avg_monetary"]) - (item[1]["avg_recency"] * 10), # Heuristic score
        reverse=True # Highest score first
    )

    # Assign segment names based on rank (assuming k=4, from best to worst)
    cluster_segment_map = {}
    segment_names = ["Loyal", "Aktif", "Potensial", "Pasif"] # Ordered from best to worst
    for i, (cluster_id, _) in enumerate(ranked_clusters):
        if i < len(segment_names):
            cluster_segment_map[cluster_id] = segment_names[i]
        else:
            cluster_segment_map[cluster_id] = f"Cluster {cluster_id}"


    results_with_segments = []
    for point, label in zip(points, labels):
        segment_label = cluster_segment_map.get(label, "Unknown")
        results_with_segments.append((point, label, segment_label))

    return results_with_segments


def _broadcast_segments(db: Session):
    """Helper to recalculate and broadcast segments."""
    try:
        segments_raw = segment_customers(db, k=4)
        segments_data = [
            SegmentItem(
                user_id=point.user_id,
                name=point.name,
                recency=point.recency,
                frequency=point.frequency,
                monetary=point.monetary,
                cluster=label,
                customer_segment=segment_label,
            ).model_dump(mode="json")
            for point, label, segment_label in segments_raw
        ]
        anyio.from_thread.run(broadcaster.broadcast, {"type": "segment_updated", "data": segments_data})
    except Exception:
        # Silently fail if broadcasting segments doesn't work.
        pass

```
###  Path: `/app/services/user_service.py`

```py
from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserUpdate


def update_user(db: Session, current_user: User, user_update: UserUpdate) -> User:
    # Check if a new email is provided and if it's already registered by another user
    if user_update.email is not None and user_update.email != current_user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
            )

    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user


```
###  Path: `/app/utils/broadcast.py`

```py
import asyncio
from typing import Any, List


class Broadcaster:
    """Manages SSE client connections and broadcasts messages."""

    def __init__(self):
        self.queues: List[asyncio.Queue] = []
        self._lock = asyncio.Lock()

    async def subscribe(self) -> asyncio.Queue:
        """Subscribes a client by creating and returning a new queue."""
        queue = asyncio.Queue()
        async with self._lock:
            self.queues.append(queue)
        return queue

    async def unsubscribe(self, queue: asyncio.Queue):
        """Unsubscribes a client by removing their queue."""
        async with self._lock:
            if queue in self.queues:
                self.queues.remove(queue)

    async def broadcast(self, message: Any):
        """Broadcasts a message to all subscribed clients."""
        # The message is cloned for each queue to prevent one consumer
        # from affecting others if the message object is mutable.
        async with self._lock:
            for queue in self.queues:
                await queue.put(message)


# Global singleton instance
broadcaster = Broadcaster()

```
###  Path: `/app/utils/priority.py`

```py
import pickle
import os
import numpy as np
from datetime import datetime, timedelta
import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Model storage path
MODEL_PATH = "priority_model.pkl"

# Global variables for the loaded model components
loaded_model = None
loaded_preprocessor = None
cluster_to_priority_map = {}

def _generate_synthetic_data(num_samples=1000):
    """Generates synthetic data for training the K-means model."""
    data = {
        'diff_days': np.random.randint(0, 90, num_samples), # 0 to 90 days out
        'status': np.random.choice(['pending', 'dp', 'paid'], num_samples),
        'price_locked': np.random.randint(100000, 5000000, num_samples), # 100k to 5M
        'jumlah_client': np.random.randint(1, 5, num_samples) # 1 to 4 clients
    }
    return data

def train_and_save_model():
    """Trains the K-means model and saves it along with the preprocessor."""
    print("Training K-means model for booking priority...")
    synthetic_data = _generate_synthetic_data()
    df = pd.DataFrame(synthetic_data)

    # Define preprocessing steps
    numeric_features = ['diff_days', 'price_locked', 'jumlah_client']
    categorical_features = ['status']

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ],
        remainder='passthrough' # Keep other columns if any, though not strictly needed here
    )

    # Create a pipeline with preprocessor and KMeans
    pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('kmeans', KMeans(n_clusters=3, random_state=42, n_init=10))])

    pipeline.fit(df)

    kmeans_model = pipeline.named_steps['kmeans']
    preprocessor_model = pipeline.named_steps['preprocessor']
    
    # Get centroids in the transformed space
    centroids_transformed = kmeans_model.cluster_centers_

    # Get the StandardScaler and OneHotEncoder components
    scaler = preprocessor_model.named_transformers_['num']
    onehot_encoder = preprocessor_model.named_transformers_['cat']

    # Determine the number of features created by the one-hot encoder
    num_onehot_features = len(onehot_encoder.get_feature_names_out(categorical_features))
    num_numeric_features = len(numeric_features)

    # To score clusters, we'll evaluate their centroids
    # Extract only the numeric parts of the centroids and inverse transform them
    numeric_centroids_transformed = centroids_transformed[:, :num_numeric_features]
    numeric_centroids_original = scaler.inverse_transform(numeric_centroids_transformed)

    # Calculate a composite score for each cluster based on its original-scale numeric features
    # Lower diff_days is better (higher urgency), higher price_locked and jumlah_client are better
    cluster_scores = []
    for i, centroid_numeric in enumerate(numeric_centroids_original):
        diff_days, price_locked, jumlah_client = centroid_numeric
        # Adjust weights as needed
        score = (price_locked * 0.5) - (diff_days * 1000) + (jumlah_client * 50000) 
        cluster_scores.append({'cluster_id': i, 'score': score})

    # Sort clusters by their score in descending order
    cluster_scores.sort(key=lambda x: x['score'], reverse=True)

    # Assign priority segments based on sorted scores
    global cluster_to_priority_map
    cluster_to_priority_map = {}
    
    # Assuming n_clusters=3 for 'high', 'medium', 'low'
    priority_labels = ['high', 'medium', 'low']
    urgency_labels = ['urgent', 'soon', 'upcoming']
    monetary_labels = ['vip', 'premium', 'regular']
    priority_scores = [90, 60, 20]

    for i, cluster_info in enumerate(cluster_scores):
        cluster_id = cluster_info['cluster_id']
        if i < len(priority_labels):
            cluster_to_priority_map[cluster_id] = {
                "priority_score": priority_scores[i],
                "priority_segment": priority_labels[i],
                "urgency_level": urgency_labels[i],
                "monetary_level": monetary_labels[i],
            }
        else:
            # Fallback for more clusters than defined labels
            cluster_to_priority_map[cluster_id] = {
                "priority_score": 0, "priority_segment": "low", "urgency_level": "upcoming", "monetary_level": "regular"
            }
```