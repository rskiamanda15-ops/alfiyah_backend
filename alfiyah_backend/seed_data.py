from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select, text
import pandas as pd
import random
import uuid
from datetime import datetime # Ensure datetime is imported for strptime

from app.core.database import SessionLocal, Base, engine
from app.models import Package, ServiceType, User, Transaction # Ensure Transaction model is imported
from app.utils.priority import train_and_save_model # Import the training function
from app.core.security import get_password_hash # Import here for password hashing
from app.utils.priority import calculate_priority # Import calculate_priority here for use in seeding transactions


def _seed_users_from_csv(db: Session):
    print("Seeding users from datasets.csv...")
    try:
        df = pd.read_csv('datasets.csv')
    except FileNotFoundError:
        print("datasets.csv not found. Skipping user seeding from CSV.")
        return

    existing_emails = set(db.query(User.email).all())
    
    for index, row in df.iterrows():
        name = str(row['Nama']).strip()
        address = str(row['Alamat']).strip()

        # Generate email based on name and address to increase uniqueness for multiple entries with same name
        base_email_identifier = f"{name.lower().replace(' ', '.')}.{address.lower().replace(' ', '')}"
        email = f"{base_email_identifier}@gmail.com"
        
        email_counter = 1
        while (email,) in existing_emails:
            email = f"{base_email_identifier}{email_counter}@gmail.com"
            email_counter += 1
        
        user = db.scalar(select(User).filter_by(email=email))
        if not user: # If user with this generated email doesn't exist, create it
            # Generate random password
            random_password = str(uuid.uuid4())[:8] # 8-character random password
            hashed_password = get_password_hash(random_password)

            # Generate random phone number (e.g., 081234567890)
            phone_number = "08" + ''.join(random.choices('0123456789', k=10))
            
            user = User(
                name=name,
                email=email,
                address=address,
                phone_number=phone_number,
                hashed_password=hashed_password,
                role="customer",
            )
            db.add(user)
            existing_emails.add((email,)) # Add to set to prevent duplicate email generation within the same run
            # print(f"Added user: {name} with email {email}") # Optional: for debugging
    db.commit()
    print("Users from datasets.csv seeded successfully.")


def _seed_transactions_from_csv(db: Session):
    print("Seeding transactions from datasets.csv...")
    try:
        df = pd.read_csv('datasets.csv')
    except FileNotFoundError:
        print("datasets.csv not found. Skipping transaction seeding from CSV.")
        return

    # Delete existing transactions to ensure a clean re-seed
    db.query(Transaction).delete()
    db.commit()
    print("Existing transactions cleared.")

    # Load users for quick lookup by name and address
    users_by_name_address = {}
    for user in db.query(User).all():
        key = (user.name, user.address)
        users_by_name_address[key] = user

    # Load service types for quick lookup and mapping
    service_types_with_packages = db.query(ServiceType).options(joinedload(ServiceType.package)).all()
    
    # Pre-process service types for efficient matching based on keywords in *existing* service data
    service_type_candidates_by_keyword = {} # {keyword: [ServiceType1, ServiceType2]}
    for st in service_types_with_packages:
        st_name_lower = st.name.lower()
        package_name_lower = st.package.name.lower() if st.package else ""

        # Map ServiceType to its own name (for exact/partial matching)
        service_type_candidates_by_keyword.setdefault(st_name_lower, []).append(st)
        
        # Map ServiceType to common keywords it contains
        if "party" in st_name_lower or "party" in package_name_lower:
            service_type_candidates_by_keyword.setdefault("party", []).append(st)
        if "wisuda" in st_name_lower or "wisuda" in package_name_lower:
            service_type_candidates_by_keyword.setdefault("wisuda", []).append(st)
        if "ramah tamah" in st_name_lower or "ramah tamah" in package_name_lower:
            service_type_candidates_by_keyword.setdefault("ramah tamah", []).append(st)
        if "engagement" in st_name_lower or "lamaran" in package_name_lower:
            service_type_candidates_by_keyword.setdefault("engagement", []).append(st)
        if "prewedding" in st_name_lower:
            service_type_candidates_by_keyword.setdefault("prewedding", []).append(st)
        if "foto ijazah" in st_name_lower:
            service_type_candidates_by_keyword.setdefault("foto ijazah", []).append(st)
        if "bridesmaid" in st_name_lower:
            service_type_candidates_by_keyword.setdefault("bridesmaid", []).append(st)
        
        # Fallback mappings for 'Penari' and 'Yudisium' if no direct ST exists
        # These are mapped to a generic category if they don't match specifically
        if "penari" in st_name_lower: # if ServiceType name itself contains "penari"
            service_type_candidates_by_keyword.setdefault("penari", []).append(st)
        elif "party" in st_name_lower or "party" in package_name_lower: # map to a generic party if possible
            service_type_candidates_by_keyword.setdefault("penari_fallback", []).append(st) 
        
        if "yudisium" in st_name_lower: # if ServiceType name itself contains "yudisium"
            service_type_candidates_by_keyword.setdefault("yudisium", []).append(st)
        elif "wisuda" in st_name_lower or "wisuda" in package_name_lower: # map to a generic wisuda if possible
            service_type_candidates_by_keyword.setdefault("yudisium_fallback", []).append(st)


    transactions_to_add = []
    
    for index, row in df.iterrows():
        nama_csv = str(row['Nama']).strip()
        alamat_csv = str(row['Alamat']).strip()
        jenis_makeup_csv_raw = str(row['Jenis_Makeup']).strip()
        jenis_makeup_csv = jenis_makeup_csv_raw.lower()
        tanggal_acara_str = str(row['Tanggal_Acara']).strip()
        tanggal_booking_str = str(row['Tanggal_Booking']).strip()
        jumlah_client = row['Jumlah_Client']

        # User Lookup
        user_key = (nama_csv, alamat_csv)
        user = users_by_name_address.get(user_key)
        if not user:
            print(f"Warning: User '{nama_csv} ({alamat_csv})' not found. Skipping transaction.")
            continue

        # ServiceType Lookup Strategy
        matched_st = None
        # 1. Try exact match of CSV Jenis_Makeup to existing service types by their name
        if jenis_makeup_csv in service_type_candidates_by_keyword:
            matched_st = random.choice(service_type_candidates_by_keyword[jenis_makeup_csv])
        else:
            # 2. Try matching CSV Jenis_Makeup against common keywords
            if "party" in jenis_makeup_csv:
                if "party" in service_type_candidates_by_keyword: matched_st = random.choice(service_type_candidates_by_keyword["party"])
            elif "wisuda" in jenis_makeup_csv:
                if "wisuda" in service_type_candidates_by_keyword: matched_st = random.choice(service_type_candidates_by_keyword["wisuda"])
            elif "ramah tamah" in jenis_makeup_csv:
                if "ramah tamah" in service_type_candidates_by_keyword: matched_st = random.choice(service_type_candidates_by_keyword["ramah tamah"])
            elif "engagement" in jenis_makeup_csv or "prewedding" in jenis_makeup_csv:
                if "engagement" in service_type_candidates_by_keyword: matched_st = random.choice(service_type_candidates_by_keyword["engagement"])
            elif "foto ijazah" in jenis_makeup_csv:
                if "foto ijazah" in service_type_candidates_by_keyword: matched_st = random.choice(service_type_candidates_by_keyword["foto ijazah"])
            elif "bridesmaid" in jenis_makeup_csv:
                if "bridesmaid" in service_type_candidates_by_keyword: matched_st = random.choice(service_type_candidates_by_keyword["bridesmaid"])
            # Special handling for "Penari" and "Yudisium" if they didn't match directly
            elif "penari" in jenis_makeup_csv:
                if "penari" in service_type_candidates_by_keyword: matched_st = random.choice(service_type_candidates_by_keyword["penari"])
                elif "penari_fallback" in service_type_candidates_by_keyword: matched_st = random.choice(service_type_candidates_by_keyword["penari_fallback"])
            elif "yudisium" in jenis_makeup_csv:
                if "yudisium" in service_type_candidates_by_keyword: matched_st = random.choice(service_type_candidates_by_keyword["yudisium"])
                elif "yudisium_fallback" in service_type_candidates_by_keyword: matched_st = random.choice(service_type_candidates_by_keyword["yudisium_fallback"])
            
        if not matched_st:
            print(f"Warning: ServiceType for '{jenis_makeup_csv_raw}' not found. Skipping transaction for {nama_csv}.")
            continue

        # Date Conversion
        try:
            tanggal_acara = datetime.strptime(tanggal_acara_str, '%Y-%m-%d')
            tanggal_booking = datetime.strptime(tanggal_booking_str, '%Y-%m-%d')
        except ValueError:
            print(f"Warning: Invalid date format for '{nama_csv}'. Skipping transaction.")
            continue

        # Create Transaction
        transaction = Transaction(
            user_id=user.id,
            service_type_id=matched_st.id,
            price_locked=matched_st.price,
            status="paid",  # Default status for historical data
            tanggal_booking=tanggal_booking,
            tanggal_acara=tanggal_acara,
            jumlah_client=jumlah_client,
        )
        
        # Calculate priority using K-means model
        priority_result = calculate_priority(transaction)
        transaction.priority_score = priority_result["priority_score"]
        transaction.priority_segment = priority_result["priority_segment"]
        transaction.urgency_level = priority_result["urgency_level"]
        transaction.monetary_level = priority_result["monetary_level"]
        transaction.updated_priority_at = datetime.utcnow() # Set current time for priority update

        transactions_to_add.append(transaction)
        
    db.add_all(transactions_to_add)
    db.commit()
    print(f"Successfully seeded {len(transactions_to_add)} transactions from datasets.csv.")


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

    # Train and save the K-means model for booking priority
    train_and_save_model()

    try:
        # Seed admin user
        admin_user = db.scalar(select(User).filter_by(email="admin@gmail.com"))
        if not admin_user:
            # get_password_hash already imported at the top
            admin_user = User(
                name="Admin User",
                email="admin@gmail.com",
                address="Admin Address",
                phone_number="081234567890",
                hashed_password=get_password_hash("admin123"),
                role="admin",
            )
            db.add(admin_user)
            print("Admin user 'admin@gmail.com' added.")

        # Seed users from CSV
        _seed_users_from_csv(db)

        # Define packages and their service types based on the Alfiyah_Makeup_Services.md file
        packages_data = {
            "Makeup Party": {
                "description": "Daftar layanan makeup untuk pesta.",
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
            "Makeup Wisuda Premium": {
                "description": "Daftar layanan makeup wisuda premium.",
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
                ],
            },
            "Makeup Wisuda Exclusive": {
                "description": "Daftar layanan makeup wisuda eksklusif.",
                "service_types": [
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
                "description": "Daftar layanan makeup lamaran dan prewedding.",
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

        # Seed transactions from CSV
        _seed_transactions_from_csv(db)

    finally:
        db.close()


if __name__ == "__main__":
    seed()
    print("Seed data inserted or updated.")