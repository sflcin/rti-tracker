import datetime

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from utils import UtilsAuth

router = APIRouter()

@router.post("/session")
async def login(request: Request, data: OAuth2PasswordRequestForm = Depends()):
    user = await UtilsAuth.AuthenticateUser(data.username, data.password)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password",
        )
    
    access_token = UtilsAuth.CreateAccessToken(
        data={"id": str(user.id), "sub": user.username,},
        expires_delta=datetime.timedelta(hours=24),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
