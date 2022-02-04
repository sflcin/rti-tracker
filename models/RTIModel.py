from tortoise import models, fields

from models.RTIUserModel import User
# import models as myModels

class RTIInfo(models.Model):
    id = fields.IntField(pk=True)
    totalNumOfRTI = fields.IntField()
    totalNumOfPendingRTI = fields.IntField()
    totalNumOfCompleteRTI = fields.IntField()
    totalNumOfIncompleteRTI = fields.IntField()
    totalNumOfForwardedRTI = fields.IntField()

class RTI(models.Model):
    """RTI Model Class"""

    id = fields.UUIDField(pk=True)
    createdOn = fields.DatetimeField(auto_now_add=True)
    updatedOn = fields.DatetimeField(auto_now=True)
    uploadedBy: fields.ForeignKeyRelation[User] = fields.ForeignKeyField("models.User")
    nameOfRti = fields.CharField(default="", max_length=500, null=False)
    whenWasRtiFiled = fields.DatetimeField()
    isFirst = fields.BooleanField(default=True)
    isLast = fields.BooleanField(default=False)
    isForwarded = fields.BooleanField(default=False)
    isDenied = fields.BooleanField(default=False)
    isPending = fields.BooleanField(default=False)
    fileType = fields.CharField(default="PDF", max_length=3, null=False)

    # extensions should be .pdf | .png
    # make a check in the frontend, there will also be a check in backend
    fileName = fields.CharField(default="", max_length=260, null=False) # including file ext
    nextRTI = fields.CharField(max_length=36)
    prevRTI = fields.CharField(max_length=36)

    async def save(self, *args, **kwargs) -> None:
        await super().save(*args, **kwargs)
