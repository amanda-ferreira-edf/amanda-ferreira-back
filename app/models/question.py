from sqlalchemy import Column, Integer, String, Boolean, JSON
from app.database import Base

class Question(Base):
    __tablename__ = "Question"
    
    questionId = Column(Integer, primary_key=True, index=True, autoincrement=True)
    questionText = Column(String, nullable=False)
    questionSubtext = Column(String, nullable=True)
    typeResponse = Column(String, nullable=False)
    multipleChoice = Column(Boolean, nullable=True)
    choices = Column(JSON, nullable=True)

class QuestionList(Base):
    __tablename__ = "QuestionList"
    
    question_list_id = Column(Integer, primary_key=True, index=True)
    question_id = Column(String, nullable=False)
