from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Users(Base):
    __tablename__ = "User"
    
    idUser = Column(String, primary_key=True, index=True)
    email = Column(String, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=True)
    role = Column(String, nullable=False)
    account_google = Column(Boolean, nullable=False)
    sended = Column(Boolean, nullable=False)
