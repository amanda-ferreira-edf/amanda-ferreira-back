from pydantic import BaseModel
from app.schemas.user import UserOut
from app.schemas.question import QuestionOut
from typing import Optional
class AnswerBase(BaseModel):
    response : str | None = None
    idUser : str
    idQuestion : int

class AnswerOut(AnswerBase):
    idAnswer : int
    user: UserOut
    question: QuestionOut
    class Config:
        from_attributes = True

class AnswerCreate(AnswerBase):
    pass

