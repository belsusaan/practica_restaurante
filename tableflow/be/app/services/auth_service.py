from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.repositories import user_repo
from app.schemas.user import UserCreate
from app.schemas.token import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# hashing
def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# Token
def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.token_expire_minutes
    )
    to_encode = {"exp": expire, "sub": str(user_id)}
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def decode_token(token: str) -> TokenData:
    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=[settings.algorithm]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise JWTError()
        return TokenData(user_id=int(user_id))
    except JWTError:
        raise JWTError("Could not validate credentials")


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


def login(db: Session, username: str, password: str) -> str | None:
    user = user_repo.get_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        return None
    return create_access_token(user.id)
