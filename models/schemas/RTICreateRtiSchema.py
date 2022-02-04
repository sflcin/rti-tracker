from typing import Optional

from tortoise.contrib.pydantic.base import PydanticModel
from pydantic import BaseModel

class CreateRTIIn(BaseModel):
    nameOfRti: str
    whenWasRtiFiled: str # epoch
    isFirst: bool
    isLast: bool
    isForwarded: bool
    isDenied: bool
    isPending: bool
    fileType: str
    fileName: str
    nextRTI: Optional[str]
    prevRTI: Optional[str]


class UpdateRTIIn(BaseModel):
    nameOfRti: str
    whenWasRtiFiled: str # epoch
    isFirst: bool
    isLast: bool
    isForwarded: bool
    isDenied: bool
    isPending: bool
    fileType: str
    fileName: str
    nextRTI: Optional[str]
    prevRTI: Optional[str]
