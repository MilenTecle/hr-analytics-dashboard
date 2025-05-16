from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL

# Create the engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base calss for models
Base = declarative_base()


# Dependency that provides a database session to route functions.
# Ensures each request gets its own session and is properly closed afterward.
def get_db():
    print("Opening DB session")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()