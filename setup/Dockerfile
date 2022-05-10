FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1

RUN apt update && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt -y install gcc python3-dev libpq-dev
RUN pip install --upgrade pip && \
    pip install psycopg2 pydantic SQLAlchemy Faker

ADD . .
ENTRYPOINT ["python", "src/main.py"]
