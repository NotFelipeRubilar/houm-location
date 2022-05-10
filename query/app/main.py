import datetime

from app.schemas import MovementsResponse, VisitsResponse
from app.services import DbService, MovementsService, VisitsService
from fastapi import Depends, FastAPI, Query, Response

app = FastAPI()


async def get_db_service() -> DbService:
    return DbService()


async def get_visits_service(db_service: DbService = Depends(get_db_service)) -> VisitsService:
    return db_service


async def get_movements_service(
    db_service: DbService = Depends(get_db_service),
) -> MovementsService:
    return db_service


@app.get("/health")
async def health_check() -> Response:
    return {"status": "ok"}


@app.get("/visits", response_model=VisitsResponse)
async def get_visits(
    user_id: int = Query(..., title="User ID", description="ID of the Houmer"),
    date: datetime.date = Query(..., title="Date", description="Date of the visit"),
    visits_service: VisitsService = Depends(get_visits_service),
) -> VisitsResponse:
    """Returns the location and the time spent in the properties visited by the given Houmer on the given date

    Args:
        user_id (int): ID of the Houmer.
        date (datetime.date): Date of the visit".

    Returns:
        VisitsResponse: A list of the locations of all the properties visited by the Houmer on the
            given date and the amount of time they spent there.
    """
    return VisitsResponse(
        user_id=user_id, date=date, visits=visits_service.get_visits(user_id, date)
    )


@app.get("/movements", response_model=MovementsResponse)
async def get_movements(
    user_id: int = Query(..., title="User ID", description="ID of the Houmer"),
    date: datetime.date = Query(..., title="Date", description="Date of the visit"),
    min_speed: float = Query(
        ..., title="Min Speed", description="Minimum speed of the movements in km/h"
    ),
    movements_service: MovementsService = Depends(get_movements_service),
) -> MovementsResponse:
    """Returns the movements made by the given Houmer on the given date where the average speed was
    over the given minimum speed

    Args:
        user_id (int): ID of the Houmer.
        date (datetime.date): Date of the visit.
        min_speed (float): Minimum speed of the movements (in km/h).

    Returns:
        MovementsResponse: A list of all the movements made by the Houmer on the given date where
            the average speed was over the given minimum.
    """
    return MovementsResponse(
        user_id=user_id,
        date=date,
        speed=min_speed,
        movements=movements_service.get_movements(user_id, date, min_speed),
    )
