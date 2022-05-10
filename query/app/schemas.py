import datetime
from typing import List

from pydantic import BaseModel


class Visit(BaseModel):
    property_id: int
    latitude: float
    longitude: float
    duration: float


class VisitsResponse(BaseModel):
    user_id: int
    date: datetime.date
    visits: List[Visit] = []


class Movement(BaseModel):
    start: datetime.datetime
    end: datetime.datetime
    total_distance: float
    duration: float
    average_speed: float


class MovementsResponse(BaseModel):
    user_id: int
    date: datetime.date
    speed: float
    movements: List[Movement] = []
