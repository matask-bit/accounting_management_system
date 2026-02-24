from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.deps import get_current_user, get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientOut, ClientUpdate

router = APIRouter(prefix="/clients", tags=["clients"])

@router.post("/", response_model=ClientOut, status_code=status.HTTP_201_CREATED)
def create_client(
    data: ClientCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    client = Client(user_id=user.id, **data.model_dump())
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

@router.get("/", response_model=list[ClientOut])
def list_clients(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Client).filter(Client.user_id == user.id).all()

@router.put("/{client_id}", response_model=ClientOut)
def update_client(
    client_id: UUID,
    data: ClientUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    client = (
        db.query(Client)
        .filter(Client.id == client_id, Client.user_id == user.id)
        .first()
    )
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(client, key, value)

    db.commit()
    db.refresh(client)
    return client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: UUID,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    client = (
        db.query(Client)
        .filter(Client.id == client_id, Client.user_id == user.id)
        .first()
    )
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()
    return None
