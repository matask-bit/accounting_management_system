from pydantic import BaseModel, EmailStr, Field
from uuid import UUID
from typing import Optional


class ClientCreate(BaseModel):
    name: str
    country_code: str = Field(min_length=2, max_length=2)
    vat_id: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    country_code: Optional[str] = Field(default=None, min_length=2, max_length=2)
    vat_id: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None


class ClientOut(BaseModel):
    id: UUID
    name: str
    country_code: str
    vat_id: Optional[str]
    email: Optional[EmailStr]
    address: Optional[str]

    class Config:
        from_attributes = True
