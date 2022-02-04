from tortoise import models, fields
from datetime import datetime
from enum import Enum
from models.RTIUserModel import User


class RTIStateEnum(str, Enum):
    RTIStateNew = "New"
    RTIStateComplete = "Complete"
    RTIStateDenied = "Denied"
    RTIStateCont = "ContinuationOfPreviousRTI"


class RTISubStateEnum(str, Enum):
    RTISubStateResponded = "Responded"
    RTISubStateNull = ""


class RTIInfo(models.Model):
    id = fields.IntField(pk=True)
    totalNumOfRTI = fields.IntField()
    totalNumOfPendingRTI = fields.IntField()
    totalNumOfCompleteRTI = fields.IntField()
    totalNumOfDeniedRTI = fields.IntField()


class RTI(models.Model):
    """RTI Model Class"""

    id = fields.UUIDField(pk=True)
    createdOn = fields.DatetimeField(auto_now_add=True)
    updatedOn = fields.DatetimeField(auto_now=True)
    uploadedBy: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User")
    nameOfRti = fields.CharField(default="", max_length=500, null=False)
    whenWasRtiFiled = fields.DatetimeField()
    stateOfRti = fields.CharEnumField(RTIStateEnum, default=RTIStateEnum.RTIStateNew)
    subStateOfRti = fields.CharEnumField(
        RTISubStateEnum, default=RTISubStateEnum.RTISubStateNull
    )
    responseOfRti = fields.ForeignKeyField(
        "models.RTIResponse", related_name="response", null=True
    )
    isResponseToResponse = fields.ForeignKeyField(
        "models.RTIResponse", related_name="response_to_response", null=True
    )
    fileType = fields.CharField(default="PDF", max_length=3, null=False)
    # extensions should be .pdf | .png
    # make a check in the frontend, there will also be a check in backend
    fileName = fields.CharField(
        default="", max_length=260, null=False
    )  # including file ext
    nextRTI = fields.CharField(max_length=36)
    prevRTI = fields.CharField(max_length=36)

    async def save(self, *args, **kwargs) -> None:
        await super().save(*args, **kwargs)

    async def update_from_dict(self, data) -> None:
        temp = data["whenWasRtiFiled"]
        data["whenWasRtiFiled"] = datetime.fromtimestamp(int(temp))
        await super().update_from_dict(data)

    class Meta:
        ordering = ["-whenWasRtiFiled"]


class RTIResponse(models.Model):
    """RTI Response Model Class"""

    id = fields.UUIDField(pk=True)
    createdOn = fields.DatetimeField(auto_now_add=True)
    updatedOn = fields.DatetimeField(auto_now=True)
    # isResponseToWhatRti: fields.ForeignKeyRelation[RTI] = fields.ForeignKeyField("models.RTI")
