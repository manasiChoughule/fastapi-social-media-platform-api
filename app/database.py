from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras  import RealDictCursor
import time
from .config import settings

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind = engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# continuously try to connect to server till it connects, we are not using it, this is done to connect diretly to the sql server. Instead of this we are connecting to sqlalchmy.
""" while True:        
    try:
        #conn = psycopg.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = 'postgres')

        conn = psycopg2.connect(dbname='fastapi',user='postgres',password='postgres'
                                ,cursor_factory=RealDictCursor)
        
        cursor = conn.cursor()
        print("Database connection was successfull!")
        break
    # else wait for 2 seconds
    except Exception as error:
        print("Connection to Database failed")
        print("Error: ", error)
        time.sleep(2) """