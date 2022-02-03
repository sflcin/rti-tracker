from fastapi import APIRouter

from api.RTIAPIV1.endpoints.RTIAuthApi import router as RTIAuthApiRouter
from api.RTIAPIV1.endpoints.RTIApi import router as RTIApiRouter

api_router = APIRouter()
api_router.include_router(RTIAuthApiRouter, prefix="/auth", tags=["Login"])
api_router.include_router(RTIApiRouter, prefix="/rti", tags=["RTI"])
