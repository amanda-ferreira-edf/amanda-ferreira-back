from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.question import QuestionListOut, QuestionOut, QuestionBase, QuestionCreate, QuestionUpdate
from app.models.question import Question, QuestionList
from app.database import get_db

router = APIRouter()


@router.get("/question-lists/{question_list_id}", response_model=QuestionListOut)
async def get_question_list(question_list_id: int, db: Session = Depends(get_db)):
    db_question_list = db.get(QuestionList, question_list_id)
    if not db_question_list:
        raise HTTPException(status_code=404, detail="Question list not found")

    return db_question_list

@router.put("/update-question-list", response_model=QuestionListOut)
async def update_question_list(question_list: QuestionListOut , db: Session = Depends(get_db)):

    db_question_list = db.get(QuestionList, question_list.question_list_id)
    if not db_question_list:
        raise HTTPException(status_code=404, detail="Question list not found")

    db_question_list.question_id = question_list.question_id
    db_question_list.question_list_id = question_list.question_list_id
    db.commit()
    db.refresh(db_question_list)
    return db_question_list

@router.get("/questions", response_model=List[QuestionOut])
async def get_all_question(question_list_id: Optional[int] = Query(None),db: Session = Depends(get_db)):
    if question_list_id is None:
        return db.query(Question).order_by(Question.questionId).all()
    else:
        question_list = db.query(QuestionList).get(question_list_id)
        if not question_list or question_list.question_id == '':
            return []

        # Lista de IDs na ordem correta
        question_ids = [int(q_id) for q_id in question_list.question_id.split(',')]

        # Buscar perguntas no banco
        questions = db.query(Question).filter(Question.questionId.in_(question_ids)).all()

        # Criar um dicionário para mapear ID -> pergunta
        question_map = {q.questionId: q for q in questions}

        # Ordenar as perguntas de acordo com question_ids
        ordered_questions = [question_map[q_id] for q_id in question_ids if q_id in question_map]

        return ordered_questions

@router.patch("/update-question", response_model=QuestionOut)
async def update_question_partial(question: QuestionUpdate, db: Session = Depends(get_db)):
    # Buscar a questão pelo ID
    db_question = db.get(Question, question.questionId)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    # Atualizar apenas os campos que vierem no request
    for key, value in question.dict(exclude_unset=True).items():
        if key != "questionId":  # não altere o ID
            setattr(db_question, key, value)
    
    db.commit()
    db.refresh(db_question)
    return db_question

@router.post("/create-question", response_model=QuestionOut)
async def create_question(question: QuestionCreate, db: Session = Depends(get_db)):
    db_question = Question(**question.dict())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

@router.delete("/delete-question", response_model=QuestionOut)
async def delete_question(questionId: int, db: Session = Depends(get_db)):
    db_question = db.get(Question, questionId)
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    db.delete(db_question)
    db.commit()
    return db_question