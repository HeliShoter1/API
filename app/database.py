from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time 
from psycopg2.extras import RealDictCursor
import psycopg2

SQLALCHEMY_DATABASE_USER = 'postgresql://postgres:19092003@localhost/FastAPI'    

engine = create_engine(SQLALCHEMY_DATABASE_USER)

Sessionlocal = sessionmaker(autocommit= False,autoflush=False,bind= engine)

Base = declarative_base()

def get_db():
    db = Sessionlocal()
    try: 
        yield db
    finally:
        db.close()

while True:
    try:
        conn = psycopg2.connect(host="localhost", database="FastAPI",user="postgres",password="19092003",cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successfully")
        break
    except Exception as error:
        print("Database connection was false")
        print("Error: " ,error)
        time.sleep(2)