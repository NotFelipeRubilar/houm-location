import datetime
from abc import ABC, abstractmethod
from typing import List

from app.db.client import get_db_client
from app.db.queries import find_movements_for_user_on_date, find_visits_for_user_on_date
from app.schemas import Movement, Visit


class VisitsService(ABC):
    @abstractmethod
    def get_visits(self, user_id: int, date: datetime.date) -> List[Visit]:
        """Return all visits of the user in the given date

        Args:
            user_id (int): ID of the user
            date (datetime.date): Date of the visit

        Returns:
            List[Visit]: A list of all visits made by the user on the given date
        """
        raise NotImplementedError()


class MovementsService(ABC):
    @abstractmethod
    def get_movements(self, user_id: int, date: datetime.date, min_speed: float) -> List[Movement]:
        """Return all movements of the user over the given min_speed in the given date

        Args:
            user_id (int): ID of the user
            date (datetime.date): Date of the movement
            min_speed (float): Minimum speed (in km/h)

        Returns:
            List[Movement]: A list of all movements made by the user on the given date where the
                average speed was over min_speed
        """
        raise NotImplementedError()


class DbService(VisitsService, MovementsService):
    def __init__(self) -> None:
        self.database = get_db_client()

    def get_visits(self, user_id: int, date: datetime.date) -> List[Visit]:
        """Return all visits of the user in the given date

        Args:
            user_id (int): ID of the user
            date (datetime.date): Date of the visit

        Returns:
            List[Visit]: A list of all visits made by the user on the given date
        """
        session = self.database.get_session()
        visits = find_visits_for_user_on_date(session, user_id, date)
        print(visits)
        return [
            Visit(
                property_id=v["property_id"],
                latitude=v["latitude"],
                longitude=v["longitude"],
                duration=v["duration"].total_seconds(),
            )
            for v in visits
        ]

    def get_movements(self, user_id: int, date: datetime.date, min_speed: float) -> List[Movement]:
        """Return all movements of the user over the given min_speed in the given date

        Args:
            user_id (int): ID of the user
            date (datetime.date): Date of the movement
            min_speed (float): Minimum speed (in km/h)

        Returns:
            List[Movement]: A list of all movements made by the user on the given date where the
                average speed was over min_speed
        """
        session = self.database.get_session()
        movements = find_movements_for_user_on_date(session, user_id, date)
        return [
            Movement(
                start=m["start"]["timestamp"],
                end=m["end"]["timestamp"],
                total_distance=m["distance"],
                duration=m["duration"],
                average_speed=m["speed"],
            )
            for m in movements
            if m["speed"] > min_speed
        ]
