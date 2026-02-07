from __future__ import annotations

import random
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Iterable

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.user import User


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


def segment_customers(db: Session, k: int) -> list[tuple[RfmPoint, int]]:
    points = build_rfm_points(db)
    if not points:
        return []
    vectors, _, _ = _normalize(points)
    labels = _kmeans(vectors, k=k)
    return list(zip(points, labels))
