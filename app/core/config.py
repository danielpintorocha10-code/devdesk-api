import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("POSTGRES_USER", "devdesk_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "devdesk_password")
POSTGRES_DB = os.getenv("POSTGRES_DB", "devdesk_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5433")

SECRET_KEY = os.getenv("SECRET_KEY", "devdesk-development-secret-change-me")

DATABASE_URL = (
    "postgresql+psycopg://"
    f"{quote_plus(POSTGRES_USER)}:{quote_plus(POSTGRES_PASSWORD)}@"
    f"{POSTGRES_HOST}:{POSTGRES_PORT}/{quote_plus(POSTGRES_DB)}"
)
