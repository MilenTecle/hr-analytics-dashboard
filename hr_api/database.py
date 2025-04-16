from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# load .env variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Create the engine and session
engine = create_engine("DATABASE_URL")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base calss for models
Base = declarative_base()