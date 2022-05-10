from functools import lru_cache

from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.engine import url
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.orm.session import Session


class PostgreSQLClient:
    def __init__(self) -> None:
        self._connection_string = url.URL(
            drivername="postgresql+psycopg2",
            username=settings.db_user,
            password=settings.db_password,
            host=settings.db_host,
            port=settings.db_port,
            database=settings.db_name,
        )
        self._engine = create_engine(self._connection_string)
        self._Session = sessionmaker(bind=self._engine)

    def get_session(self) -> Session:
        """Get a session object to make queries with

        Returns:
            Session: A session object
        """
        return self._Session()


@lru_cache(maxsize=1)
def get_db_client() -> PostgreSQLClient:
    """Return a (cached) connection to the DB

    Returns:
        PostgreSQLClient: A client to connect to the DB
    """
    return PostgreSQLClient()


BaseModel = declarative_base()
