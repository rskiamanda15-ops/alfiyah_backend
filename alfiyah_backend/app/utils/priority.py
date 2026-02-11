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
