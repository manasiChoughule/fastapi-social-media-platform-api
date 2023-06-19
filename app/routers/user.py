from sqlalchemy.orm import Session
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List
from ..database import get_db
from .. import models, schemas, utils

# connects to app in main.py
router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.UserOut)
def create_posts(user : schemas.UserCreate, db: Session = Depends(get_db)):
      
    # Hash the password
    hashed_password = utils.hash(user.password)  
    user.password = hashed_password
    new_user = models.User(**user.dict()) # unpacks dictionary in required format
    db.add(new_user)
    db.commit()
    db.refresh(new_user) # retrive the new post we committed and store back into new_post
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail = f"The user {id} does not exist.")

    return user