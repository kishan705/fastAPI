#routers/post.py

from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List,Optional
from sqlalchemy import func

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.post("/", response_model=schemas.PostResponse)
def create_post(post: schemas.Post, 
                db: Session = Depends(get_db),
                current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    new_post = models.Post(
        title=post.title,
        content=post.content,
        owner_id=int(current_user.id) 
    )

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
            db: Session = Depends(get_db), 
            current_user: schemas.TokenData = Depends(oauth2.get_current_user),
            limit : int = 10,
            skip : int = 0,
            search : Optional[str]=""
            ):
    
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.title.contains(search))\
        .limit(limit).offset(skip).all()
    
    return posts



@router.get("/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db), 
             current_user: schemas.TokenData = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes"))\
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)\
        .group_by(models.Post.id)\
        .filter(models.Post.id == id).first()
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
        
    return post