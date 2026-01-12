from fastapi import APIRouter, HTTPException, Form, Depends
from typing import List
from app.schemas.user import UserCreate, UserOut
from jose import jwt
from app.api.v1.users import create_user
from app.database import get_db
from app.models.users import Users
from app.utils.security import verify_password
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.schemas.auth import LoginDTO
import os
import requests
router = APIRouter()


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

@router.post("/auth")
def login(user: LoginDTO, db: Session = Depends(get_db)):
    existing_user = db.query(Users).filter(
        Users.email == user.email,
        Users.account_google == False
    ).first()
    
    if not existing_user:
        raise HTTPException(status_code=401, detail="Usuario ou senha incorretos")
    if verify_password(user.password, existing_user.password) == False:
        raise HTTPException(status_code=401, detail="Usuario ou senha incorretos")
    # userDb['account_google'] = False
    
    token = create_access_token({"sub": str(existing_user.idUser), "email": existing_user.email,  "role": existing_user.role})

    return {"access_token": token, "token_type": "bearer", "user": {"idUser": existing_user.idUser, 
                                                                    "email": existing_user.email, 
                                                                    "name": existing_user.name,
                                                                    "role": existing_user.role,
                                                                    "sended": existing_user.sended}}
@router.post("/auth/google")
def login_google(credential: str = Form(...), db: Session = Depends(get_db)):
    try:
        userInfo = verify_google_token(credential)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    # Aqui você pode validar o token do Google e gerar JWT
    existing_user = db.query(Users).filter(
        Users.email == userInfo["email"],
        Users.account_google == True
    ).first()
    if not existing_user:
        existing_user = create_user(
            UserCreate(
                email=userInfo["email"],
                password=None,
                idUser=userInfo["google_id"],
                name=userInfo["name"],
                role="user",
                account_google=True,
                sended=False
            ),
            db
        )       
    token = create_access_token({"sub": str(existing_user.idUser), "email": existing_user.email,  "role": existing_user.role})

    return {"access_token": token, "token_type": "bearer", "user": {"idUser": existing_user.idUser, 
                                                                    "email": existing_user.email, 
                                                                    "name": existing_user.name,
                                                                    "role": existing_user.role,
                                                                    "sended": existing_user.sended}}
def verify_google_token(token: str):
    idInfo = jwt.get_unverified_claims(token)

    response = requests.get('https://oauth2.googleapis.com/tokeninfo?id_token=' + token)

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Token inválido")

    data = response.json()

    if data['aud'] != GOOGLE_CLIENT_ID:
        raise HTTPException(status_code=401, detail="Token inválido")
    # Aqui você pode verificar o token do Google
    return {
        "email": data['email'],
        "name": data.get('name'),
        "google_id": data.get('sub'),
        "picture": data.get('picture')
    }

def create_access_token(data: dict):
    to_encode = data.copy()
    print(ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt