from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import Base, engine
from app.routers import auth, services, bookings

app = FastAPI(title="Alfiyah Booking API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(services.router, prefix="/services", tags=["services"])
app.include_router(bookings.router, prefix="/bookings", tags=["bookings"])


@app.get("/health")
def health_check():
    return {"status": "ok"}
