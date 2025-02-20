FROM python:3.13-rc-slim

# Set working directory
WORKDIR /app

# Install poetry
RUN pip install poetry

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Install dependencies without installing the project itself
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy application code
COPY . .

# Command to run the application
CMD ["gunicorn", "--config", "gunicorn_config.py", "run:app"] 