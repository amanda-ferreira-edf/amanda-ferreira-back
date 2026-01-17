from fastapi import APIRouter, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.answer import AnswerBase, AnswerOut
from app.models.answer import Answer
from app.database import get_db
import uuid

router = APIRouter()

# @router.post("/response", response_model=ResponseOut)
# def create_update_response(response: ResponseBase):
#     for u in fake_db.values():
#         if u["email"] == user.email and u["account_google"] == user.account_google:
#             raise HTTPException(status_code=400, detail="Usuário já existe com este email e tipo de conta")
    
#     if user.idUser == None:
#         user.idUser = str(uuid.uuid4())

#     fake_db[user.idUser] = user.dict()
#     return fake_db[user.idUser]

@router.post("/answer", response_model=Optional[AnswerOut])
def create_update_answer(answer: AnswerBase, db: Session = Depends(get_db)):
    db_answer = db.query(Answer).filter(Answer.idUser == answer.idUser, Answer.idQuestion == answer.idQuestion).first()
    if db_answer:
        if answer.response == None or answer.response == "":
            db.delete(db_answer)
            db.commit()
            return JSONResponse(content={"success": True})
        db_answer.response = answer.response
        db.commit()
        db.refresh(db_answer)
        return db_answer
    if answer.response == None or answer.response == "":
        return None
    db_answer = Answer(**answer.dict())
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return db_answer


@router.get("/answers", response_model=List[AnswerOut])
def list_answers_user(userId: str, db: Session = Depends(get_db)):
    answers = db.query(Answer).filter(Answer.idUser == userId).all()
    return answers

