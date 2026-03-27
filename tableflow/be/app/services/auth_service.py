from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app import models
import os
from app.config import settings
from app.repositories import user_repo
from app.schemas.user import UserCreate
from app.schemas.token import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "tu_llave_secreta_super_segura")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


# hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Token
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
        return TokenData(user_id=int(user_id))
    except (jwt.JWTError, ValueError):
        return None


# Bussines oprerations
def register(db: Session, user_data: UserCreate):
    hashed_pwd = hash_password(user_data.password)
    return user_repo.create(
        db,
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_pwd,
        full_name=user_data.full_name,
        role="waiter",
    )


def login(db: Session, username: str, password: str):
    user = user_repo.get_by_username(db, username)
    if not user:
        return None

    es_valida = verify_password(password, user.password_hash)

    if not es_valida:
        return None

    return user
