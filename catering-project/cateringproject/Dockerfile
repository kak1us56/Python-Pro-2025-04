FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt-get update -y \
    && apt-get install -y build-essential \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --upgrade pip setuptools pipenv

COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy

COPY . .

EXPOSE 8000/tcp
ENTRYPOINT [ "python" ]
CMD [ "manage.py", "runserver", "0.0.0.0:8000" ]