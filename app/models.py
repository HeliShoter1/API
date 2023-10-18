from .database import Base
from sqlalchemy import *
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id = Column(INTEGER,primary_key=True,nullable=False)
    title = Column(String,nullable=False)
    content = Column(String,nullable=True)
    rating = Column(INTEGER,nullable=False)
    create_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    id_user = Column(Integer,ForeignKey("user.id",ondelete="CASCADE"),nullable=False)

    user = relationship("User")

class User(Base):
    __tablename__ = "user" 
    
    id = Column(INTEGER,primary_key=True,nullable=False)
    name = Column(String,nullable=False)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    create_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))