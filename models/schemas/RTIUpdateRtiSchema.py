from typing import Any, Optional

from tortoise.contrib.pydantic.base import PydanticModel
from pydantic import BaseModel

from models.schemas.RTICreateRtiSchema import RTIStateEnumType, RTISubStateEnumType


class UpdateRTIIn(BaseModel):
    id: str
    nameOfRti: str
    whenWasRtiFiled: str  # epoch
    stateOfRti: RTIStateEnumType
    subStateOfRti: RTISubStateEnumType
    fileType: str
    fileName: str
    nextRTI: Optional[str]
    prevRTI: Optional[str]
