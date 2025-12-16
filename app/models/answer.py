from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
class Answer(Base):
    __tablename__ = "Answer"
    idAnswer = Column(Integer, primary_key=True, index=True)
    response = Column(String, nullable=False)
    idUser = Column(String, ForeignKey("User.idUser"), nullable=False)
    idQuestion = Column(Integer, ForeignKey("Question.questionId"), nullable=False)
    user = relationship("Users")
    question = relationship("Question")
    