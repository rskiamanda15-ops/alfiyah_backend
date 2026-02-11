# 🎯 Booking Segmentation & Priority System
Backend Feature Development  
Stack: **FastAPI + SQLAlchemy + MySQL**

---

# 📌 1. Tujuan Fitur

Membangun sistem segmentasi otomatis untuk:

- Mengatur prioritas booking makeup
- Menghindari bentrok jadwal
- Mempermudah identifikasi pelanggan VIP
- Membantu pengambilan keputusan berbasis skor

Setiap booking akan memiliki:

- `priority_score`
- `priority_segment`
- `urgency_level`
- `monetary_level`

---

# 🗄️ 2. Perubahan Struktur Database

## Tambahkan Kolom Pada Tabel `bookings`

```sql
ALTER TABLE bookings
ADD COLUMN priority_score INT DEFAULT 0,
ADD COLUMN priority_segment VARCHAR(50) DEFAULT 'low',
ADD COLUMN urgency_level VARCHAR(50),
ADD COLUMN monetary_level VARCHAR(50),
ADD COLUMN updated_priority_at TIMESTAMP NULL;
```

---

# 📦 3. Contoh Data Setelah Segmentasi

```json
{
  "id": 1,
  "user_id": 3,
  "service_type_id": 2,
  "price_locked": 3500000,
  "status": "paid",
  "tanggal_booking": "2026-02-10 12:00:00",
  "tanggal_acara": "2026-02-12 12:00:00",
  "jumlah_client": 3,
  "priority_score": 92,
  "priority_segment": "high",
  "urgency_level": "urgent",
  "monetary_level": "vip"
}
```

---

# 🧮 4. Algoritma Priority Scoring

## 4.1 Urgency (Tanggal Acara)

| Selisih Hari | Score | Level |
|-------------|--------|--------|
| ≤ 2 | +40 | urgent |
| ≤ 7 | +25 | soon |
| > 7 | +10 | upcoming |

---

## 4.2 Status Pembayaran

| Status | Score |
|--------|--------|
| paid | +30 |
| dp | +20 |
| pending | +5 |

---

## 4.3 Monetary (price_locked)

| Harga | Score | Level |
|--------|--------|--------|
| ≥ 3.000.000 | +30 | vip |
| ≥ 1.500.000 | +15 | premium |
| < 1.500.000 | +5 | regular |

---

## 4.4 Jumlah Client

| Jumlah | Score |
|--------|--------|
| ≥ 3 | +15 |
| < 3 | +5 |

---

## 4.5 Segmentasi Akhir

| Total Score | Segment |
|------------|----------|
| ≥ 80 | high |
| 50–79 | medium |
| < 50 | low |

---

# 🧠 5. Implementasi FastAPI

---

## 5.1 Utility Function (utils/priority.py)

```python
from datetime import datetime

def calculate_priority(booking):
    score = 0
    today = datetime.utcnow()
    diff_days = (booking.tanggal_acara - today).days

    # Urgency
    if diff_days <= 2:
        score += 40
        urgency = "urgent"
    elif diff_days <= 7:
        score += 25
        urgency = "soon"
    else:
        score += 10
        urgency = "upcoming"

    # Status
    if booking.status == "paid":
        score += 30
    elif booking.status == "dp":
        score += 20
    else:
        score += 5

    # Monetary
    if booking.price_locked >= 3000000:
        score += 30
        monetary = "vip"
    elif booking.price_locked >= 1500000:
        score += 15
        monetary = "premium"
    else:
        score += 5
        monetary = "regular"

    # Jumlah Client
    if booking.jumlah_client >= 3:
        score += 15
    else:
        score += 5

    # Final Segment
    if score >= 80:
        segment = "high"
    elif score >= 50:
        segment = "medium"
    else:
        segment = "low"

    return {
        "priority_score": score,
        "priority_segment": segment,
        "urgency_level": urgency,
        "monetary_level": monetary
    }
```

---

# 🏗️ 6. Integrasi Saat Create Booking

## services/booking_service.py

```python
from utils.priority import calculate_priority
from datetime import datetime

def create_booking(db, booking_data):
    booking = Booking(**booking_data)

    # Hitung priority
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
```

---

# 🔄 7. Update Priority Saat Booking Diupdate

```python
def update_booking(db, booking, update_data):
    for key, value in update_data.items():
        setattr(booking, key, value)

    result = calculate_priority(booking)

    booking.priority_score = result["priority_score"]
    booking.priority_segment = result["priority_segment"]
    booking.urgency_level = result["urgency_level"]
    booking.monetary_level = result["monetary_level"]
    booking.updated_priority_at = datetime.utcnow()

    db.commit()
    db.refresh(booking)

    return booking
```

---

# 📡 8. Endpoint API

## 8.1 Get Booking Urut Prioritas

```
GET /bookings?order_by=priority_score_desc
```

Query SQL:

```sql
SELECT * FROM bookings
ORDER BY priority_score DESC;
```

---

## 8.2 Filter Berdasarkan Segment

```
GET /bookings?segment=high
```

---

# ⏰ 9. Optional: Auto Recalculate Harian

Gunakan scheduler seperti:

- APScheduler
- Celery + Redis

Flow:

```
Scheduler berjalan tiap hari
      ↓
Ambil booking yang belum selesai
      ↓
Hitung ulang priority
      ↓
Update database
```

---

# 🏁 10. Arsitektur Final

```
Booking dibuat / diupdate
        ↓
FastAPI hitung priority
        ↓
Disimpan ke database
        ↓
Flutter hanya membaca & menampilkan
```

---

# 🚀 11. Future Improvement

- Risk flag (double booking / unpaid H-1)
- Histori perubahan segmentasi
- Analitik pelanggan loyal
- Notifikasi otomatis H-1 acara
- Integrasi AI scoring

---

# ✅ Kesimpulan

Dengan sistem ini:

- Prioritas pelanggan otomatis
- Dashboard real-time
- Manajemen booking lebih terstruktur
- Sistem scalable untuk pengembangan lanjutan