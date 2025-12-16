from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from app.schemas.user import UserCreate, UserOut
from app.database import get_db
from app.models.users import Users
from app.utils.security import hash_password
import uuid

router = APIRouter()

@router.post("/user", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(
        Users.email == user.email,
        Users.account_google == user.account_google
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Usuário já existe com este email e tipo de conta")
   
    user_id = user.idUser if user.idUser else str(uuid.uuid4())

    new_user = Users(
        idUser=user_id,
        email=user.email,
        name=user.name,
        role=user.role,
        account_google=user.account_google,
        password=hash_password(user.password) if user.password else None,
        sended=user.sended
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # atualiza o objeto com dados do banco
    return new_user


@router.get("/users", response_model=List[UserOut])
def list_users(db: Session = Depends(get_db)):
    return db.query(Users).all()

