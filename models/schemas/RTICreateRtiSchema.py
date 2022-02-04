from typing import Optional, Literal

from models.RTIModel import RTIStateEnum, RTISubStateEnum
from pydantic import BaseModel

RTIStateEnumType = Literal[
    RTIStateEnum.RTIStateNew,
    RTIStateEnum.RTIStateComplete,
    RTIStateEnum.RTIStateCont,
    RTIStateEnum.RTIStateDenied,
]
RTISubStateEnumType = Literal[
    RTISubStateEnum.RTISubStateNull, RTISubStateEnum.RTISubStateResponded
]


class CreateRTIIn(BaseModel):
    nameOfRti: str
    whenWasRtiFiled: str  # epoch
    stateOfRti: RTIStateEnumType
    subStateOfRti: RTISubStateEnumType
    fileType: str
    fileName: str
    nextRTI: Optional[str]
    prevRTI: Optional[str]
