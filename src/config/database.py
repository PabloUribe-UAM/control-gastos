from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from os import getenv

# database_url = "sqlite:///./database.sqlite"
database_url = f"mysql+pymysql://root:{getenv('MYSQL_ROOT_PASSWORD')}@{getenv('MYSQL_HOST')}:{getenv('MYSQL_PORT')}/{getenv('MYSQL_DATABASE')}"

engine = create_engine(database_url)

SessionLocal = sessionmaker(bind=engine,
    autocommit=False, autoflush=False)

Base = declarative_base()