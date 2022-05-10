from app.queue import QueueService, RabbitQueueService
from app.schemas import UpdateLocationParams, User
from fastapi import Body, Depends, FastAPI, HTTPException, Response, status

app = FastAPI()


def get_queue_service() -> QueueService:
    return RabbitQueueService()


async def get_current_user(user_id: int = Body(...)) -> User:
    """Returns the authenticated user making the request. Usually this value would be extracted
    from an authentication token, but for the purposes of this test we receive it as a body param.

    Args:
        user_id (int, optional): The user_id contained in the body of the request

    Returns:
        User: _description_
    """
    return User(id=user_id, name="Juan Perez")


@app.get("/health")
async def health_check() -> Response:
    return {"status": "ok"}


@app.post("/location")
def update_location(
    params: UpdateLocationParams,
    current_user: User = Depends(get_current_user),
    queue_service: QueueService = Depends(get_queue_service),
) -> Response:
    """Receives location data from a Houmer.

    Args:
        params (UpdateLocationParams): The location of the Houmer and the timestamp of the measurement
        current_user (User, optional): The User making the request
        queue_service (QueueService, optional): A connection to the queue

    Returns:
        Response: The result of the operation
    """
    try:
        queue_service.send_message(
            {
                "latitude": params.latitude,
                "longitude": params.longitude,
                "timestamp": params.date_time.timestamp(),
                "user_id": current_user.id,
            }
        )
        return {"status": "ok"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error while saving location data.",
        )
