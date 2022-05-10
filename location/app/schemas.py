import datetime

from pydantic import BaseModel, Field


class UpdateLocationParams(BaseModel):
    latitude: float = Field(
        None, ge=-90, le=90, description="Latitude of the Houmer's current position"
    )
    longitude: float = Field(
        None, ge=-180, le=180, description="Longitude of the Houmer's current position"
    )
    date_time: datetime.datetime = Field(
        None, description="Date and time the measurement was taken"
    )


class User(BaseModel):
    id: int
    name: str
