from sqlalchemy.orm import Session
from sqlalchemy import select, text

from app.core.database import SessionLocal, Base, engine
from app.models import Package, ServiceType
from app.models.user import User


def seed() -> None:
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    # Apply schema migrations for new columns if they don't exist
    conn = engine.connect()
    try:
        # Check and add priority_score
        result = conn.execute(text("SHOW COLUMNS FROM transactions LIKE 'priority_score'")).fetchone()
        if not result:
            conn.execute(text("ALTER TABLE transactions ADD COLUMN priority_score INT DEFAULT 0"))
            print("Added column to transactions: priority_score")

        # Check and add priority_segment
        result = conn.execute(text("SHOW COLUMNS FROM transactions LIKE 'priority_segment'")).fetchone()
        if not result:
            conn.execute(text("ALTER TABLE transactions ADD COLUMN priority_segment VARCHAR(50) DEFAULT 'low'"))
            print("Added column to transactions: priority_segment")

        # Check and add urgency_level
        result = conn.execute(text("SHOW COLUMNS FROM transactions LIKE 'urgency_level'")).fetchone()
        if not result:
            conn.execute(text("ALTER TABLE transactions ADD COLUMN urgency_level VARCHAR(50)"))
            print("Added column to transactions: urgency_level")

        # Check and add monetary_level
        result = conn.execute(text("SHOW COLUMNS FROM transactions LIKE 'monetary_level'")).fetchone()
        if not result:
            conn.execute(text("ALTER TABLE transactions ADD COLUMN monetary_level VARCHAR(50)"))
            print("Added column to transactions: monetary_level")

        # Check and add updated_priority_at
        result = conn.execute(text("SHOW COLUMNS FROM transactions LIKE 'updated_priority_at'")).fetchone()
        if not result:
            conn.execute(text("ALTER TABLE transactions ADD COLUMN updated_priority_at TIMESTAMP NULL"))
            print("Added column to transactions: updated_priority_at")
        
        # Check and add phone_number to users table
        result = conn.execute(text("SHOW COLUMNS FROM users LIKE 'phone_number'")).fetchone()
        if not result:
            conn.execute(text("ALTER TABLE users ADD COLUMN phone_number VARCHAR(20)"))
            print("Added column to users: phone_number")

        conn.commit()
    except Exception as e:
        print(f"Error applying migrations: {e}")
        conn.rollback()
    finally:
        conn.close()

    try:
        # Seed admin user
        admin_user = db.scalar(select(User).filter_by(email="admin@example.com"))
        if not admin_user:
            from app.core.security import get_password_hash # Import here to avoid circular dependency
            admin_user = User(
                name="Admin User",
                email="admin@example.com",
                address="Admin Address",
                phone_number="081234567890",
                hashed_password=get_password_hash("adminpassword"),
                role="admin",
            )
            db.add(admin_user)
            print("Admin user 'admin@example.com' added.")

        # Define packages and their service types based on the Markdown file
        packages_data = {
            "Makeup Party": {
                "description": "Party-ready glam makeup",
                "service_types": [
                    {
                        "name": "Reguler Party",
                        "description": "Untuk Pesta, Foto Ijazah & Ramah-Tamah. Belum termasuk soflens & transport.",
                        "price": 200000,
                    },
                    {
                        "name": "Premium Party",
                        "description": "Untuk bridesmaid, Mom&Sist Bride, graduation SMP/SMA. Belum termasuk soflens & transport.",
                        "price": 300000,
                    },
                ],
            },
            "Makeup Wisuda": {
                "description": "Graduation makeup packages",
                "service_types": [
                    {
                        "name": "Premium Wisuda",
                        "description": "Sudah termasuk akomodasi Hotel (jika open room), Hijab do, pemasangan toga. Belum termasuk soflens. Hairdo 120-150k oleh tim. Tersedia soflens 50k (bebas pilih warna).",
                        "price": 350000,
                    },
                    {
                        "name": "Paket Ramah Tamah & Wisuda Premium",
                        "description": "Sudah termasuk akomodasi Hotel (jika open room), Hijab do, pemasangan toga. Belum termasuk soflens. Hairdo 120-150k oleh tim. Tersedia soflens 50k (bebas pilih warna).",
                        "price": 550000,
                    },
                    {
                        "name": "Exclusive Wisuda",
                        "description": "Free Hijabdo & Soflens, pemasangan toga. Hairdo 120-150k oleh tim.",
                        "price": 500000,
                    },
                    {
                        "name": "Paket Ramah Tamah & Wisuda Exclusive",
                        "description": "Free Hijabdo & Soflens, pemasangan toga. Hairdo 120-150k oleh tim.",
                        "price": 700000,
                    },
                ],
            },
            "Makeup Lamaran": {
                "description": "Engagement makeup services",
                "service_types": [
                    {
                        "name": "Exclusive Engagement",
                        "description": "Belum termasuk transport.",
                        "price": 500000,
                    },
                    {
                        "name": "Reguler Engagement",
                        "description": "Belum termasuk transport.",
                        "price": 400000,
                    },
                    {
                        "name": "Prewedding",
                        "description": "Pemasangan attire 50k. Free softlens & hijab do. Belum termasuk transport.",
                        "price": 400000,
                    },
                ],
            },
        }

        for package_name, package_data in packages_data.items():
            package_obj = db.scalar(select(Package).filter_by(name=package_name))
            if not package_obj:
                package_obj = Package(name=package_name, description=package_data["description"])
                db.add(package_obj)
                db.flush()  # Flush to get the package_obj.id

            for service_type_data in package_data["service_types"]:
                service_type_obj = db.scalar(
                    select(ServiceType).filter_by(
                        package_id=package_obj.id, name=service_type_data["name"]
                    )
                )
                if not service_type_obj:
                    db.add(
                        ServiceType(
                            package_id=package_obj.id,
                            name=service_type_data["name"],
                            description=service_type_data["description"],
                            price=service_type_data["price"],
                        )
                    )
        db.commit()
    finally:
        db.close()



if __name__ == "__main__":
    seed()
    print("Seed data inserted or updated.")
