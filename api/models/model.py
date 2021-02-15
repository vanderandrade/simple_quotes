import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import os

Base = declarative_base()
engine = db.create_engine(
    f'postgresql://'
    f'{os.environ[f"PGUSER"]}:'
    f'{os.environ[f"PGPASSWORD"]}@'
    f'{os.environ[f"PGHOST"]}:'
    f'{os.environ[f"PGPORT"]}/'
    f'{os.environ[f"PGDATABASE"]}')
db_session = sessionmaker(engine)
meta = db.MetaData()