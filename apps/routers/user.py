#routers/user.py
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, utils, schemas, oauth2  # 👈 Added oauth2 here
from ..database import get_db
from typing import List

router = APIRouter(
    prefix="/users",
    tags=['Users']
)



@router.post("/", response_model=schemas.UserResponse)
def create_user(user_det: schemas.UserCreate, db: Session = Depends(get_db)):

    existing_email = db.query(models.User).filter(models.User.email == user_det.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = utils.hash(user_det.password)
    new_user = models.User(username=user_det.username, email=user_det.email, password=hashed_pwd, is_active=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user




@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_profile(db: Session = Depends(get_db), 
                             current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    user = db.query(models.User).filter(models.User.id == int(current_user.id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user



@router.get("/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



