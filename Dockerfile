FROM python:3.10-slim

COPY Pipfile Pipfile.lock ./
RUN python -m pip install --upgrade pip
RUN pip install pipenv

WORKDIR /app
COPY . /app

# install deps
RUN apt-get -y update
RUN apt-get install -y ffmpeg

# Creates a non-root user and adds permission to access the /app folder
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser


CMD [ "python", "main.py" ]