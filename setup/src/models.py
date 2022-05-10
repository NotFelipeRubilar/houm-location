from typing import List

from engine import BaseModel
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class User(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), default="")

    locations: List["Location"] = relationship("Location", back_populates="user")


class Location(BaseModel):
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    date_time = Column(DateTime, nullable=False)

    user: User = relationship("User", back_populates="locations")


class Property(BaseModel):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(128), default="")
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
