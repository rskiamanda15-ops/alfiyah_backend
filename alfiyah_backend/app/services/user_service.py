from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserUpdate


def update_user(db: Session, current_user: User, user_update: UserUpdate) -> User:
    # Check if a new email is provided and if it's already registered by another user
    if user_update.email is not None and user_update.email != current_user.email:
        existing_user = db.query(User).filter(User.email == user_update.email).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
            )

    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)

    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

