# Use the official Python 3.11 image as a base image and name it 'builder' stage
FROM python:3.11-buster as builder

# Install the 'poetry' package manager
RUN pip install poetry==1.6.1

# Set environment variables for poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the 'pyproject.toml' and 'poetry.lock' files into the container
COPY pyproject.toml poetry.lock ./

# Install project dependencies using poetry with cache support
RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --no-dev --no-root

# Switch to a new base image for the 'runtime' stage
FROM python:3.11-slim-buster as runtime

# Set the virtual environment path and update the PATH variable
ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

# Copy the virtual environment from the 'builder' stage to the 'runtime' stage
COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

# Copy the 'backend' directory from your local context into the container
COPY backend ./backend

# Define the command to run when the container starts
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "80"]
