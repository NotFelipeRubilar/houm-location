from pydantic import BaseModel, Field


class LocationMessage(BaseModel):
    latitude: float = Field(None, ge=-90, le=90)
    longitude: float = Field(None, ge=-180, le=180)
    timestamp: float
    user_id: int
