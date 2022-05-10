import datetime

from app.db.models import Location
from sqlalchemy.orm import Session


def add_location(
    db: Session, user_id: int, latitude: float, longitude: float, date_time: datetime.datetime
) -> Location:
    loc = Location(user_id=user_id, latitude=latitude, longitude=longitude, date_time=date_time)
    with db.begin():
        db.add(loc)
    db.refresh(loc)
    return loc
