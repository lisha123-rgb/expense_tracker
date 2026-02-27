import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or os.urandom(32)

    # 👉 PostgreSQL connection from .env
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # -------------------------
    # Security Hardening
    # -------------------------
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False
    SESSION_COOKIE_SAMESITE = "Lax"

    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = False

    SESSION_PROTECTION = "strong"
    PERMANENT_SESSION_LIFETIME = 1800