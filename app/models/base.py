from datetime import datetime, timezone
from typing import Optional, Annotated, Any
from bson import ObjectId
from pydantic import BaseModel, Field, BeforeValidator, ConfigDict, field_serializer


def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if isinstance(v, str):
        if ObjectId.is_valid(v):
            return ObjectId(v)
        raise ValueError("Invalid ObjectId string")
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[ObjectId, BeforeValidator(validate_object_id)]


class BaseMongoModel(BaseModel):
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        populate_by_name=True,
        json_schema_extra={"example": {}},
    )

    id: Optional[PyObjectId] = Field(default=None, alias="_id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    @field_serializer("id", when_used="json")
    def serialize_id(self, value: Optional[ObjectId]) -> Optional[str]:
        if value is None:
            return None
        return str(value)

    def dict(self, *args: Any, **kwargs: Any) -> dict[str, Any]:
        kwargs.setdefault("exclude_none", True)
        data = super().model_dump(*args, **kwargs)
        if "_id" in data and data["_id"] is None:
            del data["_id"]
        return data
