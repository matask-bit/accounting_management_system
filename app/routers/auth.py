from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.user import UserCreate
from app.schemas.auth import Token
from app.models.user import User
from app.core.security import hash_password, verify_password, create_access_token
from app.core.deps import get_db
from app.core.errors import bad_request, unauthorized

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=Token)
def register(data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise bad_request("Email exists")
    if len(data.password) > 72:
        raise bad_request("Password too long")

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        full_name=data.full_name,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise unauthorized("Invalid credentials")

    return {"access_token": create_access_token(str(user.id)), "token_type": "bearer"}
