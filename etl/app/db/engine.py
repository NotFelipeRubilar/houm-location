from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.engine import url
from sqlalchemy.orm import declarative_base, sessionmaker

connection_string = url.URL(
    drivername="postgresql+psycopg2",
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)

BaseModel = declarative_base()
