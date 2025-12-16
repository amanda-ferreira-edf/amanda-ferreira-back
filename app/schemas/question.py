from pydantic import BaseModel
from typing import Optional, List

class QuestionBase(BaseModel):
    questionText: str
    questionSubtext: Optional[str]
    typeResponse: str
    multipleChoice: Optional[bool]
    choices: Optional[List[str]] 

class QuestionCreate(QuestionBase):
    pass

class QuestionOut(QuestionBase):
    questionId: int

    class Config:
        from_attributes = True  # permite ler objetos ORM

class QuestionUpdate(BaseModel):
    questionId: int  # obrigatório para identificar a questão
    questionText: Optional[str] = None
    questionSubtext: Optional[str] = None
    typeResponse: Optional[str] = None
    multipleChoice: Optional[bool] = None
    choices: Optional[list] = None
    
class QuestionListBase(BaseModel):
    question_list_id: int
    question_id: str

class QuestionListOut(QuestionListBase):
    pass

    class Config:
        from_attributes = True  # permite ler objetos ORM

