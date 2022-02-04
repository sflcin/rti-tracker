from pydantic import EmailStr
from models import User


async def username_exists(username: str) -> bool:
    return await User.exists(username=username)


async def email_exists(email: EmailStr) -> bool:
    return await User.exists(email=email)


def isChanged(val1, val2):
    return not (val1 == val2)
