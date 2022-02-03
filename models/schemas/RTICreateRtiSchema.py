from tortoise.contrib.pydantic.base import PydanticModel
from pydantic import BaseModel

class CreateRTIIn(BaseModel):
    nameOfRTI: str
    whenWasRtiFiled: str # epoch
    isFirst: bool
    isLast: bool
    isForwarded: bool
    isDenied: bool
    isPending: bool
    fileType: str
    fileName: str
    nextRTI: str
    prevRTI: str


class UpdateRTIIn(BaseModel):
    nameOfRTI: str
    whenWasRtiFiled: str # epoch
    isFirst: bool
    isLast: bool
    isForwarded: bool
    isDenied: bool
    isPending: bool
    fileType: str
    fileName: str
    nextRTI: str
    prevRTI: str
