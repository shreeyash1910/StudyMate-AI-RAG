import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()


# --------------------------------------------------
# DATABASE CONFIGURATION
# --------------------------------------------------

# If DATABASE_URL exists, use it.
# This will be used by Supabase/Render in production.
#
# Otherwise, use the local SQL Server database.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    DATABASE_URL = (
        "mssql+pyodbc://SHREEYASH/StudyMaterialRAG"
        "?driver=ODBC+Driver+17+for+SQL+Server"
        "&trusted_connection=yes"
    )


# --------------------------------------------------
# DATABASE ENGINE
# --------------------------------------------------

engine = create_engine(
    DATABASE_URL,
    echo=True
)


# --------------------------------------------------
# DATABASE SESSION
# --------------------------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# --------------------------------------------------
# BASE MODEL
# --------------------------------------------------

Base = declarative_base()


# --------------------------------------------------
# DATABASE DEPENDENCY
# --------------------------------------------------

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()