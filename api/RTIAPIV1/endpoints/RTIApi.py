from datetime import datetime
from typing import Union

from fastapi import APIRouter, HTTPException, Depends

from models.RTIUserModel import User
from models.RTIModel import RTI, RTIInfo
from models.RTIModel import RTIStateEnum  # , RTISubStateEnum
from models.schemas import RTICreateRtiSchema, RTIUpdateRtiSchema

from utils.Utils import isChanged

from utils.Dependencies import (
    # get_current_user,
    get_current_active_user,
    # get_current_superuser,
)

router = APIRouter()


@router.get("/get/{limit}")
async def getAllRTI(limit: Union[int, str]):
    """
    Get limited RTIs from the DB IFF `limit`: int,
    `limit`: str = "all" will result in all RTIs.
    This will also give total number of RTIs.
    """
    allRTIDict = dict()

    if type(limit) == str and limit.lower() == "all":
        totalNumberOfRTIObj = await RTIInfo.get(id=0)
        allRTIDict["totalRTIs"] = totalNumberOfRTIObj.totalNumOfRTI
        allRTIObj = await RTI.all()
    elif type(limit) == int and limit > 0:
        allRTIDict["totalRTIs"] = limit
        allRTIObj = await RTI.all()
        allRTIObj = allRTIObj[:limit]
    else:
        raise HTTPException(status_code=404, detail="limit variable isn't valid!")

    tempList = []
    for RTIObj in allRTIObj:
        RTIObjDict = dict(RTIObj)

        for itemsToBePopped in ["createdOn", "updatedOn", "uploadedBy_id"]:
            RTIObjDict.pop(itemsToBePopped)

        tempList.append(RTIObjDict)

    allRTIDict["RTIs"] = tempList

    return allRTIDict


@router.get("/get/id/{id}")
async def getRTIById(id: str):
    """
    Get RTI by id
    """
    if not await RTI.exists(id=id):
        raise HTTPException(
            status_code=404, detail="No RTI found with the provided ID!"
        )

    RTIObj = await RTI.get(id=id)

    RTIObjDict = dict(RTIObj)

    for itemsToBePopped in ["createdOn", "updatedOn", "uploadedBy_id"]:
        RTIObjDict.pop(itemsToBePopped)

    return RTIObjDict


@router.post("/create")
async def createRTI(
    content: RTICreateRtiSchema.CreateRTIIn,
    current_user: User = Depends(get_current_active_user),
):
    """
    Create RTI, this will return the whole object
    """
    _whenWasRtiFiled = datetime.fromtimestamp(int(content.whenWasRtiFiled))
    RTIObj = await RTI.create(
        nameOfRti=content.nameOfRti,
        whenWasRtiFiled=_whenWasRtiFiled,
        stateOfRti=content.stateOfRti,
        subStateOfRti=content.subStateOfRti,
        fileType=content.fileType,
        fileName=content.fileName,
        nextRTI=content.nextRTI,
        prevRTI=content.prevRTI,
        uploadedBy=current_user,
    )

    if not await RTIInfo.exists(id=0):
        raise HTTPException(
            status_code=404, detail="RTI info table doesn't have '0' id row!"
        )

    RTIInfoObj = await RTIInfo.get(id=0)

    if RTIInfoObj:
        if RTIObj.stateOfRti == RTIStateEnum.RTIStateNew:
            RTIInfoObj.totalNumOfRTI += 1
            RTIInfoObj.totalNumOfPendingRTI += 1
        if RTIObj.stateOfRti == RTIStateEnum.RTIStateComplete:
            RTIInfoObj.totalNumOfPendingRTI -= 1
            RTIInfoObj.totalNumOfCompleteRTI += 1
        if RTIObj.stateOfRti == RTIStateEnum.RTIStateDenied:
            RTIInfoObj.totalNumOfPendingRTI -= 1
            RTIInfoObj.totalNumOfDeniedRTI += 1

    await RTIInfoObj.save()

    await RTIObj.save()

    return RTIObj


@router.post("/update")
async def updateRTI(
    content: RTIUpdateRtiSchema.UpdateRTIIn,
    current_user: User = Depends(get_current_active_user),
):
    """
    Update RTI, this will return the whole object
    """
    if not await RTI.exists(id=content.id):
        raise HTTPException(
            status_code=404, detail="No RTI found with the provided ID!"
        )

    RTIObj = await RTI.get(id=content.id)
    ogState = RTIObj.stateOfRti

    # breakpoint()
    await RTIObj.update_from_dict(data=dict(content))
    currState = RTIObj.stateOfRti

    if not await RTIInfo.exists(id=0):
        raise HTTPException(
            status_code=404, detail="RTI info table doesn't have '0' id row!"
        )

    RTIInfoObj = await RTIInfo.get(id=0)

    if isChanged(currState, ogState):
        if (
            ogState == RTIStateEnum.RTIStateNew
            and currState == RTIStateEnum.RTIStateDenied
        ):
            RTIInfoObj.totalNumOfPendingRTI -= 1
            RTIInfoObj.totalNumOfDeniedRTI += 1

    await RTIInfoObj.save()

    await RTIObj.save()

    return RTIObj
