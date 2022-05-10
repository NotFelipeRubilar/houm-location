FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1

RUN apt update && \
    export DEBIAN_FRONTEND=noninteractive && \
    apt -y install gcc python3-dev libpq-dev
RUN pip install --upgrade pip && \
    pip install pipenv

WORKDIR /app
ADD Pipfile .
ADD Pipfile.lock .
RUN pipenv install --system --deploy

ADD . .
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.main:app"]
