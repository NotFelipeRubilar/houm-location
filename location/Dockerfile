FROM python:3.10-slim-bullseye

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip && \
    pip install pipenv

WORKDIR /app
ADD Pipfile .
ADD Pipfile.lock .
RUN pipenv install --system --deploy

ADD . .
ENTRYPOINT ["uvicorn", "--host", "0.0.0.0", "--port", "8000", "app.main:app"]
