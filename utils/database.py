import os
import streamlit as st
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import QueuePool
from contextlib import contextmanager
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Get database configuration from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Check if all variables exist
if not all([DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    st.error("Database configuration error: One or more environment variables are missing. Please check your .env file.")
    st.stop()

# Build the database connection URL
SQLALCHEMY_DATABASE_URL = (
    f"singlestoredb://{DB_USER}:{DB_PASSWORD}@"
    f"{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

# Create the SQLAlchemy engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    poolclass=QueuePool,
    pool_size=25,              # 🔄 2.5x increase (10 → 25)
    max_overflow=15,           # 🔄 3x increase (5 → 15)  
    pool_timeout=45,           # 🔄 Longer timeout (30 → 45s)
    pool_recycle=1800,         # Keep same (30 min)
    pool_pre_ping=True 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@contextmanager
def get_connection():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()