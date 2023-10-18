from  fastapi import *
from typing import  List
from . import  Schemas ,utils
from .database import *

router = APIRouter(
    prefix= "/users",
    tags=['User']
)

@router.get("/",response_model=List[Schemas.User])
def get_user():
    cursor.execute("""SELECT * FROM public.user order by id""")
    users = cursor.fetchall()
    return users

@router.post("/",response_model=Schemas.User)
def create_user(user: Schemas.CreateUser):
    hash_password = utils.hash(user.password)
    user.password = hash_password
    cursor.execute("""INSERT INTO public.user (name,email,password) VALUES (%s,%s,%s) RETURNING *""",(user.name,user.email,user.password))
    conn.commit()
    users = cursor.fetchone()
    return users

@router.get("/{id}",response_model=Schemas.User)
def get_user(id : int):
    cursor.execute("""SELECT * FROM public.user where id = (%s)""",(str(id)))
    user = cursor.fetchone()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    return user

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_user(id: int):
    cursor.execute("""SELECT * FROM public.user where id = (%s)""",(str(id)))
    user = cursor.fetchone()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    conn.commit()
    cursor.execute("""DELETE FROM public.user where id = (%s)""",(str(id)))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=Schemas.User)
def update_user(id: int ,new_user: Schemas.CreateUser):
    cursor.execute("""SELECT * FROM public.user where id = (%s)""",(str(id)))
    user = cursor.fetchone()
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} does not exist")
    cursor.execute("""UPDATE public.user SET name = %s, email = %s, password = %s where id = %s returning *""",(new_user.name,new_user.email,new_user.password,str(id)))
    conn.commit()
    return user
