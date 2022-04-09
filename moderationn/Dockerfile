FROM python:3.10-alpine

WORKDIR /app

RUN pip install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv sync --system
COPY . .

CMD ["uvicorn", "main:app", "--port=80"]