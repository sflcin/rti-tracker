"""
NOTE: You must create a column in RTIInfo with id=0 and other fields = 0
This is a one time thing.
"""

from sys import path

import uvicorn
import toml

from typing import MutableMapping, Any

from starlette.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from tortoise.contrib.starlette import register_tortoise

from api.RTIMotherRouter import api_router as RTIMotherRouterOfRouters
from aerichConfig import DATABASE_URL

app: FastAPI = FastAPI()

path.append(".")
config: MutableMapping[str, Any] = toml.load("config.toml")

register_tortoise(
    app, db_url=DATABASE_URL, modules={"models": ["models"]}, generate_schemas=True
)

# origins = [
#     "..."
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# This is a test api function
# Don't remove
# and it states TRUTH
@app.get("/RTIApiv1/hello")
async def test_api():
    """Test Api call. Should return {"RTI":"Tracker"}"""
    return {"RTI":"Tracker"}

app.include_router(RTIMotherRouterOfRouters, prefix="/RTIApiv1")

if config["debug"]["set"]:
    if __name__ == "__main__":
        uvicorn.run(app, host="0.0.0.0", port=8080)