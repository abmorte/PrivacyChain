from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:960113@localhost/mestrado-ifpb"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={'options': '-csearch_path={}'.format('privacychain')}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

