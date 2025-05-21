import os
from dotenv import load_dotenv

# Load environment variables from .env file in development
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Validate that the required environment variable is set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Make sure it's defined in Render env vars.")