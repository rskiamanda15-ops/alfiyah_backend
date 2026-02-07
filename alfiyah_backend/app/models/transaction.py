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
