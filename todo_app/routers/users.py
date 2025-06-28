from fastapi import APIRouter, Depends, status, Path, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from models import Todos , Users
from database import engine , SessionLocal
from typing import Annotated
from pydantic import BaseModel,Field
from routers import auth
from .auth import Users, get_current_user
from passlib.context import CryptContext


router = APIRouter(
     prefix='/user',
    tags=['user']
)


def get_db():
    db = SessionLocal()
    try:
        yield db 
    finally:
        db.close()
        
        
db_dependency= Annotated[Session,Depends(get_db)]
user_dependency= Annotated[dict,Depends(get_current_user)]

bcrypt_context = CryptContext(schemes=['bcrypt'],deprecated='auto')


class UserVerification(BaseModel):
    password: str
    new_password : str = Field(min_length=6)
    
class phone_number_update(BaseModel):
    phone_number:str
    new_phone_number:str = Field(min_length=10)

@router.get('/',status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    return db.query(Users).filter(Users.id==user.get('id')).first()

@router.put("/password",status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency,
                          user_verification:UserVerification):
    if user is None:
        raise HTTPException(status_code=401,detail='Authentication failed')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_verification.password,user_model.hashed_password):
         raise HTTPException(status_code=401,detail='Error on password changed')
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
     
    db.add(user_model)
    db.commit()  

@router.put("/phone_number",status_code=status.HTTP_204_NO_CONTENT)
async def change_phone_number(user: user_dependency, db: db_dependency,
                          update_phone_number:phone_number_update):
    if user is None:
        raise HTTPException(status_code=401,detail='user not found')
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if update_phone_number.phone_number != user_model.phone_number:
        raise HTTPException(status_code=400, detail='Current phone number does not match')

    user_model.phone_number = update_phone_number.new_phone_number
    
    
    
    db.add(user_model)
    db.commit()    
    

    