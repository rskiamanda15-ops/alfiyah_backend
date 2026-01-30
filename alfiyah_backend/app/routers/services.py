from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_admin
from app.models.service import Package, ServiceType
from app.schemas.service import PackageCreate, PackageRead, ServiceTypeCreate

router = APIRouter()


@router.get("/packages", response_model=list[PackageRead])
def list_packages(db: Session = Depends(get_db)):
    return db.query(Package).all()


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
    return package


@router.post("/types", response_model=PackageRead, status_code=status.HTTP_201_CREATED)
def create_service_type(
    payload: ServiceTypeCreate,
    db: Session = Depends(get_db),
    _admin=Depends(get_current_admin),
):
    package = db.query(Package).filter(Package.id == payload.package_id).first()
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
    db.refresh(package)
    return package
