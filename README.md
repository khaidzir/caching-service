# Caching Service

This is a simple caching service that caches two lists of strings. This has 2 main endpoints:

- `POST /payload` to create a new payload. This accepts two lists of strings, and returns the id of the created payload. If the payload is already cached, it will return the id of the existing payload. If not, it will process the payload using the `transformer_function` and cache the result.
- `GET /payload/{id}` to get the payload by id. This returns the cached payload.

The service is implemented using FastAPI and is containerized using Docker.

## Table of contents

- [Prerequisites](#prerequisites)
- [Stacks](#stacks)
- [Development mode](#development-mode)
- [Deployment](#deployment)

## Prerequisites
Before using this project, ensure you have the following prerequisites installed:

- Python 3.11+
- Docker (for building and running Docker images)
- Poetry (for dependency management)

## Stacks
- FastAPI
- PostgreSQL
- SQLAlchemy

## Development mode

### Install dependencies
```
poetry install
```

### Install pre-commit hooks
```
pre-commit install
```

### Run the tests
1. Ensure you have activated your Poetry virtual environment:
   ```
   poetry shell
   ```

2. Run the tests using pytest:
   ```
   pytest tests/
   ```

### Run the service
Make sure you have activated your Poetry virtual environment.
```
fastapi dev app/main.py
```

For the api documentation, go to `http://localhost:8000/docs`.


## Deployment
First, create a directory `pgdata` in the root of the project to store the PostgreSQL data.
```
mkdir pgdata
```

Ensure you have Docker installed and running.
```
docker compose up --build -d
```
Now you can access the api at `http://localhost:8000`.