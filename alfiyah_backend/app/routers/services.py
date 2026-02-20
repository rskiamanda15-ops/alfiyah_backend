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
