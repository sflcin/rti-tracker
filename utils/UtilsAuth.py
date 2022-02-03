from datetime import datetime, timedelta
from typing import Optional
from jose import jwt
from pydantic import EmailStr
from passlib.context import CryptContext
import toml
import email_validator

from models.RTIUserModel import User

config = toml.load("config.toml")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def IsEmail(text: EmailStr):
    try:
        email_validator.validate_email(text)
        return True
    except:
        return False


def GetPasswordHash(password: str) -> str:
    return pwd_context.hash(password)


def VerifyPassword(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def AuthenticateUser(username: str, password: str):
    if IsEmail(username):
        if not await User.exists(email=username):
            return False
        user = await User.get(email=username)
    else:
        if not await User.exists(username=username):
            return False
        user = await User.get(username=username)

    if not VerifyPassword(password, user.hashed_password):
        return False
    return user


def CreateAccessToken(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(config["jwt"]["lifetime_seconds"])
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, config["jwt"]["key"], algorithm=config["jwt"]["algorithm"]
    )
    return encoded_jwt

