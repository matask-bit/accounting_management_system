from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.schemas.tax_profile import TaxProfileCreate, TaxProfileOut, TaxProfileUpdate
from app.models.tax_profile import TaxProfile
from app.core.deps import get_db, get_current_user

router = APIRouter(prefix="/tax-profiles", tags=["tax-profiles"])

@router.post("/", response_model=TaxProfileOut, status_code=status.HTTP_201_CREATED)
def create_tax_profile(
    data: TaxProfileCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    profile = TaxProfile(user_id=user.id, **data.model_dump())
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return profile

@router.get("/", response_model=list[TaxProfileOut])
def list_tax_profiles(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(TaxProfile).filter(TaxProfile.user_id == user.id).all()

@router.get("/{profile_id}", response_model=TaxProfileOut)
def get_tax_profile(
    profile_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    profile = (
        db.query(TaxProfile)
        .filter(TaxProfile.id == profile_id, TaxProfile.user_id == user.id)
        .first()
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Tax profile not found")
    return profile

@router.put("/{profile_id}", response_model=TaxProfileOut)
def update_tax_profile(
    profile_id: UUID,
    data: TaxProfileUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    profile = (
        db.query(TaxProfile)
        .filter(TaxProfile.id == profile_id, TaxProfile.user_id == user.id)
        .first()
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Tax profile not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)
    return profile

@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tax_profile(
    profile_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    profile = (
        db.query(TaxProfile)
        .filter(TaxProfile.id == profile_id, TaxProfile.user_id == user.id)
        .first()
    )
    if not profile:
        raise HTTPException(status_code=404, detail="Tax profile not found")

    db.delete(profile)
    db.commit()
    return None
