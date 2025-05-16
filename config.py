import os
from dotenv import load_dotenv

# load .env variables
load_dotenv()

# Read the PostgreSQL connection URL from the environment
DATABASE_URL = os.getenv("DATABASE_URL")