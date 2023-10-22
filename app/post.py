from fastapi import *
from typing import List, Optional
from . import Schemas, models, oauth2
from sqlalchemy.orm import Session
from sqlalchemy import func
from .database import get_db
from fastapi.encoders import jsonable_encoder

router = APIRouter(
    prefix = "/posts",
    tags = ['Post'],
)

@router.get('/',response_model=List[Schemas.PostOut])
def get_post(db: Session = Depends(get_db),user_id : int = Depends(oauth2.get_current_user),limit: int = 10,skip: int = 0,search: Optional[str] = ""):
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_200_OK,detail=f"user with {user_id.id} is does not exist")
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model= Schemas.Post)
def create_posts(post : Schemas.CreatePost,db: Session = Depends(get_db),user : int = Depends(oauth2.get_current_user)):
    new_post = models.Post(title = post.title,content = post.content,rating = post.rating,id_user = user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=Schemas.PostOut)
def posts(id: int,db: Session = Depends(get_db),user_id : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} was not found")
    if post[0].id_user != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not autherized to perform requested action")
    return post

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int,db: Session = Depends(get_db),user_id : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    if post.first().id_user != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not autherized to perform requested action")
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model= Schemas.Post)
def update_post(id : int,post: Schemas.CreatePost, db: Session = Depends(get_db),user_id : int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {id} does not exist")
    if post_query.first().id_user != user_id.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not autherized to perform requested action")
    post_query.update({"title" : post.title,"content":post.content,"rating":post.rating},synchronize_session=False)
    db.commit()
    return post_query.first()