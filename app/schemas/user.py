# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(max_length=72)
    full_name: Optional[str] = None

class UserOut(BaseModel):
    id: UUID
    email: EmailStr
    full_name: Optional[str]

    class Config:
        from_attributes = True
