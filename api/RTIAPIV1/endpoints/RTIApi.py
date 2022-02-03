from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.exceptions import DoesNotExist

from models.RTIUserModel import User
from models.RTIModel import RTI, RTIInfo
from models.schemas import RTICreateRtiSchema

from utils import UtilsAuth

from utils.Dependencies import (
    get_current_user,
    get_current_active_user,
    get_current_superuser
)

router = APIRouter()

@router.post("/create/")
async def create_post(
    content: RTICreateRtiSchema.CreateRTIIn, current_user: User = Depends(get_current_active_user)
):
    _whenWasRtiFiled = datetime.fromtimestamp(int(content.whenWasRtiFiled))
    RTIObj = await RTI.create(
        nameOfRTI = content.nameOfRTI,
        whenWasRtiFiled = _whenWasRtiFiled,
        isFirst = content.isFirst,
        isLast = content.isLast,
        isForwarded = content.isForwarded,
        isDenied = content.isDenied,
        isPending = content.isPending,
        fileType = content.fileType,
        fileName = content.fileName,
        nextRTI = content.nextRTI,
        prevRTI = content.prevRTI ,
        uploadedBy = current_user
    )

    try:
        RTIInfoObj = await RTIInfo.get(id=0)
    except DoesNotExist:
        print("Error: RTIInfo isn't init!")

    if RTIInfoObj:
        if RTIObj.isFirst:
            RTIInfoObj.totalNumOfRTI += 1
        if RTIObj.isLast and not RTIObj.isPending and not RTIObj.isDenied:
            RTIInfoObj.totalNumOfCompleteRTI += 1
        if RTIObj.isLast and RTIObj.isDenied:
            RTIInfoObj.totalNumOfIncompleteRTI += 1
        if RTIObj.isLast and RTIObj.isDenied:
            RTIInfoObj.totalNumOfIncompleteRTI += 1
        if RTIObj.isPending:
            RTIInfoObj.totalNumOfPendingRTI += 1
        if RTIObj.isPending:
            RTIInfoObj.totalNumOfForwardedRTI += 1
    
    await RTIInfoObj.save()

    await RTIObj.save()
