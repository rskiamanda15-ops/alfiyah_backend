from sqlalchemy.orm import Session

from app.core.database import SessionLocal, Base, engine
from app.models import Package, ServiceType


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        if db.query(Package).count() > 0:
            return
        party = Package(name="Makeup Party", description="Party-ready glam makeup")
        wisuda = Package(name="Makeup Wisuda", description="Graduation makeup packages")
        db.add_all([party, wisuda])
        db.flush()

        db.add_all(
            [
                ServiceType(
                    package_id=party.id,
                    name="Premium Party",
                    description="Premium party look with styling",
                    price=750000,
                ),
                ServiceType(
                    package_id=party.id,
                    name="Exclusive Party",
                    description="Exclusive party look with luxury products",
                    price=1200000,
                ),
                ServiceType(
                    package_id=wisuda.id,
                    name="Premium Wisuda",
                    description="Premium graduation makeup",
                    price=850000,
                ),
                ServiceType(
                    package_id=wisuda.id,
                    name="Exclusive Wisuda",
                    description="Exclusive graduation makeup",
                    price=1350000,
                ),
            ]
        )
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Seed data inserted")
