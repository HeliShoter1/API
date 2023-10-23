from fastapi import *
from typing import  List
from . import  models, user, post, auth, vote
from .database import *

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
def root():
    return {"message": "HeliShoter1"}
