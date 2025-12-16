from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    idUser: str | None = None 
    name: str
    role: str
    account_google: bool
    sended: bool
    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str | None

class UserOut(UserBase):
    pass