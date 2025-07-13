# Set the python version as a build-time argument
# with Python 3.12 as the default
ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

# No virtual environment - use system Python directly
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends libpq-dev gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# MODIFIED: Fix paths - removed ./FareFly prefix
COPY ./requirements.txt .
RUN pip install --no-cache-dir psycopg2-binary
RUN pip install --no-cache-dir fastapi uvicorn sqlalchemy alembic
RUN pip install --no-cache-dir -r requirements.txt

# MODIFIED: Fix paths - removed ./FareFly prefix
COPY ./src/ /app/src/
COPY ./alembic.ini .
RUN mkdir -p /app/migrations
COPY ./migrations/ /app/migrations/

# Create startup script
RUN echo '#!/bin/bash' > start.sh && \
    echo 'echo "Starting application..."' >> start.sh && \
    echo 'echo "Database URL: ${DATABASE_URL:0:25}..."' >> start.sh && \
    echo 'alembic upgrade head || echo "Warning: Migration failed but continuing"' >> start.sh && \
    echo 'uvicorn src.app.main:app --host 0.0.0.0 --port ${PORT:-8000}' >> start.sh && \
    chmod +x start.sh

EXPOSE ${PORT}
CMD ["./start.sh"]