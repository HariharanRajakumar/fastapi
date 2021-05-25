from fastapi import APIRouter, Depends, status, HTTPException, Response
from .. import schemas, models
from ..database import get_db
from typing import List
from sqlalchemy.orm import Session
from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()


@router.post('/user', response_model=schemas.ShowUser, tags=["user"])
def create(request: schemas.User, db: Session = Depends(get_db)):
    hashedPassword = pwd_cxt.hash(request.password)
    new_user = models.User(email=request.email,
                           username=request.name, password=hashedPassword)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get('/user/{id}', response_model=schemas.ShowUser, tags=["user"])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id {id} NOT FOUND")
    return user
