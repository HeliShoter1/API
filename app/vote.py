from fastapi import *
from typing import List, Optional
from . import Schemas, models, oauth2
from sqlalchemy.orm import Session
from .database import get_db

router = APIRouter(
    prefix = "/vote",
    tags = ['Vote'],
)

@router.post('/',status_code= status.HTTP_201_CREATED)
def create_vote(vote: Schemas.Vote,db: Session = Depends(get_db), cr_user : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == cr_user.id)
    fisrt_vote = vote_query.first()
    if (vote.dir == 1):
        if fisrt_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail= f"user {cr_user.id} has alrealy voted on post{vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id,user_id = cr_user.id)
        db.add(new_vote)
        db.commit()
        return {'message:': "successfully added vote"}
    else :
        if not fisrt_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message:" : "successfully delete vote"}