import datetime

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from models.RTIUserModel import User, UserPydantic, UserInPydantic
from utils import UtilsAuth, Utils

router = APIRouter()


@router.post("/session")
async def login(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    user = await UtilsAuth.AuthenticateUser(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=400,
            detail="Incorrect username or password",
        )

    access_token = UtilsAuth.CreateAccessToken(
        data={
            "id": str(user.id),
            "sub": user.username,
        },
        expires_delta=datetime.timedelta(hours=24),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/register", response_model=UserPydantic)
async def create_user(user: UserInPydantic):
    if not await Utils.username_exists(user.username):
        if not await Utils.email_exists(user.email):
            # add hashed password
            temp = user.dict(exclude_unset=True)
            temp["hashed_password"] = UtilsAuth.GetPasswordHash(user.password)
            # finally create object
            user_obj = await User.create(**temp)
            # save object
            return await UserPydantic.from_tortoise_orm(user_obj)
        else:
            raise HTTPException(
                status_code=403,
                detail="Email already exists",
            )
    else:
        raise HTTPException(
            status_code=403,
            detail="Username already exists",
        )
