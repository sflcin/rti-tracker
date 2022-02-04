from tortoise import models, fields
from tortoise.contrib.pydantic import pydantic_model_creator, pydantic_queryset_creator
from pydantic import EmailStr, AnyHttpUrl
from pydantic.schema import schema

from models.schemas.RTIUserSchema import UserIn
from utils import ExtraFields


class User(models.Model):
    """
    User Model Class
    - Base class with basic functionality
    """

    id = fields.UUIDField(pk=True)
    username = fields.CharField(max_length=15, unique=True, null=False)
    email: EmailStr = ExtraFields.EmailField(index=True, unique=True, null=False)
    hashed_password = fields.CharField(default="", max_length=500, null=False)
    is_active = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)
    created_on = fields.DatetimeField(auto_now_add=True)
    updated_on = fields.DatetimeField(auto_now=True)

    # async def save(self, *args, **kwargs) -> None:
    #     self.id = str(self.id)
    #     await super().save(*args, **kwargs)

    class PydanticMeta:
        exclude = [
            "hashed_password",
            "is_active",
            "is_superuser",
            "create_on",
            "updated_on",
        ]


##############################
##### PYDANCTIC SCHEMAS ######
##############################

## Schemas for User

UserPydantic = pydantic_model_creator(User, name="User", exclude=["created_on"])
UserPydanticList = pydantic_queryset_creator(User)
UserInPydantic = UserIn
