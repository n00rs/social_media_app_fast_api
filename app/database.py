from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

# data base url
# postgresql://<username>:<password>@<ip@address/host>/<dbname>

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_host}:{settings.database_port}/{settings.database_name}"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_pg_connection():
    # while True:
        try:
            # - *dbname*: the database name
            # - *database*: the database name (only as keyword argument)
            # - *user*: user name used to authenticate
            # - *password*: password used to authenticate
            # - *host*: database host address (defaults to UNIX socket if not provided)
            # - *port*: connection port number (defaults to 5432 if not provided)
            conn = psycopg2.connect(f"dbname={settings.database_name} user={settings.database_username} password={settings.database_password} host={settings.database_host}",cursor_factory=RealDictCursor)
            cursor = conn.cursor() 
            print("Database connection succesfull")
            return cursor
            # break
        except Exception as err:
            print("Database connection failed")
            print(err)
            time.sleep(2)    
