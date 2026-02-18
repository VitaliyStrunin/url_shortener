import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path(__file__).parent.parent

load_dotenv(dotenv_path / '.env')

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 5432)
DB_NAME = os.getenv("DB_NAME", "shortener_db")

DB_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

MAX_CODE_GENERATION_ATTEMPTS=10
CODE_LENGTH = 10
