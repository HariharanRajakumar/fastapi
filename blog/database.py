from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import databases,sqlalchemy


SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:hariharan2003#@localhost:5432/blog'

# SQLALCHEMY_DATABASE_URL='sqlite:///./blog.db'
engine=create_engine(SQLALCHEMY_DATABASE_URL)
database = databases.Database(SQLALCHEMY_DATABASE_URL)
metadata = sqlalchemy.MetaData()



SessionLocal = sessionmaker(bind=engine,autocommit=False,autoflush=False)

Base = declarative_base()


def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()