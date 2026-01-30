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
