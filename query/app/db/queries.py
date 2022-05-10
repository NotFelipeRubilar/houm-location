import datetime
from typing import Dict, List

from app.utils import get_metric_distance
from sqlalchemy.orm import Session
from sqlalchemy.sql import text

visits_query = """
SELECT s.user_id, p.id as property_id, s.latitude, s.longitude, s.start_time, s.end_time, s.duration
FROM (
	SELECT user_id, latitude, longitude, grp, min(date_time) as start_time, max(date_time) as end_time, max(date_time) - min(date_time) as duration
	FROM (
	  SELECT user_id, date_time, latitude, longitude, count(is_reset) OVER (ORDER BY date_time) AS grp
	  FROM (
	    SELECT
		    user_id,
	    	date_time,
	    	latitude,
	    	longitude,
	    	CASE
	    		WHEN lag(latitude) OVER (ORDER BY date_time) <> latitude or lag(longitude) OVER (ORDER BY date_time) <> longitude
	    		THEN 1
	    	END AS is_reset
	    FROM locations
	    WHERE user_id = :user_id and DATE(date_time) = :date
	  ) AS t
	) AS g
	GROUP BY user_id, latitude, longitude, grp
	ORDER BY min(date_time)
) s
INNER JOIN properties p
    ON p.latitude = s.latitude AND p.longitude = s.longitude
WHERE duration >= '00:05:00'
ORDER BY s.start_time;
"""


def find_visits_for_user_on_date(db: Session, user_id: int, date: datetime.date) -> List[Dict]:
    """Find all visits a user made on a given date. For the purposes of this test, a Visit is
    a period of time where the user remains at least 5 minutes at a location that matches the
    coordinates of an existing property.

    Args:
        db (Session): Session object
        user_id (int): ID of the user
        date (datetime.date): Date of the visits

    Returns:
        List[Dict]: A list of all visits made by the user on the given date
    """
    with db.begin():
        results = db.execute(
            text(visits_query), {"user_id": user_id, "date": date.strftime("%Y-%m-%d")}
        )
    return results.all()


def find_movements_for_user_on_date(db: Session, user_id: int, date: datetime.date):
    """Find all movements a user made on a given date. For the purposes of this test, a Movement is
    the period of time between two consecutive Visits. The distance is the difference (in meters) between the
    locations of the visited properties, and the duration is the total amount of seconds spent moving from one
    property to the next. The speed is the distance divided by the duration, expressed in km/h.

    Args:
        db (Session): Session object
        user_id (int): ID of the user
        date (datetime.date): Date of the visits

    Returns:
        _type_: _description_
    """
    visits = find_visits_for_user_on_date(db, user_id, date)
    print(visits)
    movements: List[Dict] = []
    for i, v in enumerate(visits):
        if i + 1 == len(visits):
            break

        data = {
            "user_id": v["user_id"],
            "start": {
                "latitude": v["latitude"],
                "longitude": v["longitude"],
                "timestamp": v["end_time"],
            },
            "end": {
                "latitude": visits[i + 1]["latitude"],
                "longitude": visits[i + 1]["longitude"],
                "timestamp": visits[i + 1]["start_time"],
            },
        }
        data["distance"] = get_metric_distance(
            lat_i=v["latitude"],
            long_i=v["longitude"],
            lat_j=visits[i + 1]["latitude"],
            long_j=visits[i + 1]["longitude"],
        )
        data["duration"] = (visits[i + 1]["start_time"] - v["end_time"]).total_seconds()
        data["speed"] = (data["distance"] / data["duration"]) * 3.6  # m/s -> km/h
        movements.append(data)
    return movements
